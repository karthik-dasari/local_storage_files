from flask import Flask,jsonify
import os,time,schedule


app=Flask(__name__)


@app.route('/getcameras')
def getcameras():
    os.chdir('app/hls')
    cameras=[]
    for camera_id in os.listdir():
        cameras.append(camera_id)
    os.chdir('../..')
    return jsonify(cameras)

@app.route('/<camera_id>')
def getvideos(camera_id):
    os.chdir('app/hls/'+camera_id)
    videos=[]
    for datetime_string in os.listdir():
        videos.append(datetime_string)
    os.chdir('../../..')
    return jsonify(videos)

@app.route('/<string:camera_id>/<string:datetime_string>/stream.m3u8')
def index(camera_id,datetime_string):
    os.chdir('app/hls')
    if not os.path.exists(camera_id):
        return "Camera ID "+camera_id+" not found"
    else:
        os.chdir(camera_id)
        if not os.path.exists(datetime_string):
            return "Stream not found on this date:"+datetime_string
        else:
            os.chdir(datetime_string)
            with open('stream.m3u8', 'r') as playlist:
                ts_filenames = [line.rstrip() for line in playlist
                                if line.rstrip().endswith('.ts')]
            data={'list_of_streams': ts_filenames}
            os.chdir('../../../..')
            return jsonify(data)



def clean():
    os.chdir('hls')
    for camera_id in os.listdir():
        os.chdir(camera_id)
        for datetime_string in os.listdir():
            if time.time()-os.path.getmtime(datetime_string)>604800:
                os.system('rm -rf '+datetime_string)
        os.chdir('..')
    os.chdir('..')

schedule.every().day.at("01:00").do(clean)

    
if __name__ == '__main__':
    app.run(debug=True)
    while True:
        schedule.run_pending()
        time.sleep(60)