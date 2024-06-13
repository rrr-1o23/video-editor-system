import socket
import glob
import json
import sys
import os

# MP4ファイルの一覧表示及び選択
def files_view():
    print('')
    files = glob.glob('./data/*.mp4')
    for i in range(len(files)):
        print(files[i], '->', i+1)
    print('')
    data_num = int(input('Select the data number you want to send to the server from above. \n-> '))
    filename = os.path.basename(files[data_num-1])

    val = input(f'Are you sure it is {filename}? (y/n) -> ')
    if val.upper() == 'Y' or val.upper() =='YES':
        return filename
    else:
        print('Start over ...')
        return files_view()

# ファイルのサイズ確認
def byte_check(filepath):
    file_size = os.path.getsize(filepath)/(10**6)
    
    if 10**3 <= file_size:
        print(f'Selected file bytes: {file_size/(10**3):.2f}GB')
    else:
        print(f'Selected file bytes: {file_size:.2f}MB')

    if file_size > pow(2, 32):
            raise Exception('File must be below 2GB.')


# 変換方法の選択
def input_cmd():
    cmd_list = {
            1:'compress', 
            2:'change_resolution', 
            3:'change_aspect_ratio', 
            4:'convert_to_audio', 
            5:'convert_to_gif'
        }
    print('')
    for key, value in cmd_list.items():
        print(f'{key}: {value}')
    print('')
    cmd_num = int(input('Please enter a number. -> '))

    if 1 <= cmd_num or cmd_num <= 5:
        return cmd_num
    else:
        return input_cmd()
    
def mmp(cmd_num, filepath):
    filename = os.path.basename(filepath)
    ext = os.path.splitext(filename)[1][1:]
    #JSONデータを構築
    dict = {
        'command_number': str(cmd_num),
        'filename': filename,
    }
    json_str = json.dumps(dict).encode() # JSONに変換

    with open(filepath, 'rb') as f:
        f.seek(0, os.SEEK_END)
        file_size = f.tell()
        f.seek(0,0)
    
    json_size = len(json_str).to_bytes(16, 'big')
    media_type = ext.encode('utf-8')
    type_size = len(media_type).to_bytes(1, 'big')
    payload_size = file_size.to_bytes(47, 'big')

    #print('JSON_SIZE:', len(json_str))
    #print('MEDIA_SIZE:',len(media_type))
    #print('PAYLOAD_SIZE:', file_size)

    header = json_size + type_size + payload_size
    body = json_str + media_type

    data = header + body

    return data

def mmp_decode(data):
    header = data[:64]
    json_size = int.from_bytes(header[:16], 'big')
    type_size = int.from_bytes(header[16:17], 'big')
    payload_size = int.from_bytes(header[17:], 'big')
 
    body = data[64:]
    json_str = body[:json_size].decode()
    data_dict = json.loads(json_str)
    media_type = body[json_size:json_size+type_size].decode()

    return data_dict, media_type, payload_size
    
####################################################
    
def main():
    server_address = '0.0.0.0'
    server_port = 9001
    stream_rate = 4096

    # 作業ディレクトリに'./data'フォルダがあるか確認
    dpath = './data'
    if not os.path.exists(dpath):
        print('Data directory does not exist.')
        print('Create a ''data'' directory and save the mp4 files in the directory.')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print('connection to {}'.format(server_address, server_port))

    try:
        sock.connect((server_address, server_port))
    except socket.error as err:
        print(err)
        sys.exit(1)

    filename = files_view()
    filepath = './data' + '/' + filename
    byte_check(filepath)
    cmd_num = input_cmd()

    try:
        sock.sendall(mmp(cmd_num, filepath))
        print('The transmission of the header has been completed.')

        with open(filepath, 'rb') as f:
            data = f.read(stream_rate)
            while data:
                print('Sending')
                sock.send(data)
                data = f.read(stream_rate)
        
        print("Transmission of MP4 file completed!")
        
        output_header = sock.recv(4096)
        data_dict, media_type, payload_size = mmp_decode(output_header)

        #print('')
        #print('DATA_DICT:', data_dict)
        #print('MEDIA_TYPE:', media_type)
        #print('PAYLOAD_SIZE', payload_size)
        #print('')
        print('Recived output_header!')

        filename = data_dict['filename']

        with open('./output/' + filename, 'wb') as f:
            while True:
                data = sock.recv(stream_rate)
                if not data:
                    break
                f.write(data)

        print(f'Recived {filename}')

    except socket.error as err:
        print(err)
        sys.exit(1)

    finally:
        print("closing socket")
        sock.close()



main()

