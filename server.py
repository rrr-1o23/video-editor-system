import socket
import ffmpeg # type: ignore
import glob
import json
import sys
import os

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

# 動画圧縮
def compress_video(input_file, output_file, bitrate='500k'):
    ffmpeg.input(input_file).output(output_file, b=bitrate).run()
# 解像度の変更
def change_resolution(input_file, output_file, resolution='720x480'):
    ffmpeg.input(input_file).output(output_file, vf=f"scale={resolution}").run()
# 動画のアスペクト比の変更
def change_aspect_ratio(input_file, output_file, aspect_ratio='1:1'):
    ffmpeg.input(input_file).output(output_file, vf=f"scale=640:640,setsar={aspect_ratio}").run()
# 動画をオーディオに変換
def convert_to_audio(input_file, output_file):
    ffmpeg.input(input_file).output(output_file, acodec='mp3').run()
# 時間範囲でのGIFの作成
def convert_to_gif(input_file, output_file, start_time, duration, fps=10):
    ffmpeg.input(input_file, ss=start_time, t=duration).output(output_file, vf=f"fps={fps}", pix_fmt='rgb24').run()

# コマンドによって処理分け
def data_conversion(cmd_num, filepath):
    filename = os.path.splitext(os.path.basename(filepath))[0]

    if cmd_num == '1':
        output_filepath = './temp/' + filename + '_compress.mp4'
        compress_video(filepath, output_filepath)
        return output_filepath
    elif cmd_num == '2':
        output_filepath = './temp/' + filename + '_change_resolution.mp4'
        change_resolution(filepath, output_filepath)
        return output_filepath
    elif cmd_num == '3':
        output_filepath = './temp/' + filename + '_change_aspect_ratio.mp4'
        change_aspect_ratio(filepath, output_filepath)
        return output_filepath
    elif cmd_num == '4':
        output_filepath = './temp/' + filename + '_audio.mp3'
        convert_to_audio(filepath, output_filepath)
        return output_filepath
    elif cmd_num == '5':
        output_filepath = './temp/' + filename + '.gif'
        convert_to_gif(filepath, output_filepath)
        return output_filepath
    else:
        pass

def mmp(cmd_num, filepath):
    filename = os.path.basename(filepath)
    ext = os.path.splitext(filename)[1][1:]
    print(ext)
    #JSONデータを構築
    dict = {
        'command_number': str(cmd_num),
        'filename': filename,
    }
    print(dict)
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

    print(len(header))
    data = header + body

    return data

###################################################
def main():
    server_address = '0.0.0.0'
    server_port = 9001
    stream_rate = 4096

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 作業ディレクトリに'./temp'フォルダがあるか確認
    dpath = './temp'
    if not os.path.exists(dpath):
        os.makedirs(dpath)

    print('Starting up on {} port {}'.format(server_address, server_port))

    sock.bind((server_address, server_port))
    sock.listen(1)

    while True:
        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)

            header = connection.recv(1024)
            data_dict, media_type, payload_size = mmp_decode(header)

            #print('')
            #print('DATA_DICT:', data_dict)
            #print('MEDIA_TYPE:', media_type)
            #print('PAYLOAD_SIZE', payload_size)
            #print('')
            #print('recived header!')

            # mp4ファイルの受け取り
            filepath = os.path.join(dpath, data_dict['filename']) 
            with open(filepath, 'wb') as f:
                while payload_size > 0:
                    data = connection.recv(min(payload_size, stream_rate))
                    f.write(data)
                    print(f'reciced {len(data)} bytes')
                    payload_size -= len(data)
            #print('Recived MP4 file!')
            #print('')
            cmd_num = data_dict['command_number']
            #print('cmd_num:', cmd_num)

            output_filepath = data_conversion(cmd_num, filepath)
            os.remove(filepath) # オリジナルファイルの削除

            connection.sendall(mmp(cmd_num, output_filepath))

            
            with open(output_filepath, 'rb') as f:
                while True:
                    data = f.read(4096)
                    if not data:
                        break
                    connection.sendall(data)
            
            os.remove(output_filepath) # クライアントに送信後，変換済みファイルを駆除


        except Exception as e:
                print('Error: ' + str(e))
        
        finally:
            print('Closing current connection')
            connection.close()
        

main()
