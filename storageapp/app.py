# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from storageapp.database import db_session, init_engine
from storageapp.models import ClipMetadata
from storageapp.logger import get_logger, set_logger_params
from sqlalchemy import and_
from clip_manager import ClipManager

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('storageapp.default_settings')
app.config.from_pyfile('application.cfg', silent=True)

clip_manager = None

def init_app():
    set_logger_params(app)
    init_engine(app.config['DATABASE_URI'], convert_unicode=True)
    
    global clip_manager
    clip_manager = ClipManager(app.config)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/get_meta', methods=['GET', 'POST'])
def get_meta():
    stream_id = int(request.args.get('stream_id'))
    start_time = float(request.args.get('start_time'))
    stop_time = float(request.args.get('stop_time'))
    
    if stream_id == None or start_time == None or stop_time == None :
        return jsonify(error_message='Not all parameters supplied'), 402
    
    if start_time > stop_time :
        return jsonify(error_message='Incorrect time interval'), 402
    
    
    clip_metas = ClipMetadata.query.filter(and_(    \
        ClipMetadata.stream_id == stream_id,        \
        ClipMetadata.start_time < stop_time,        \
        ClipMetadata.stop_time > start_time))
        
    json_clip_metas = [] 
    
    for c in clip_metas :
        json_clip_metas.append(c.to_json())
    
    result = { 'clips' : json_clip_metas }
    return jsonify(**result)


@app.route('/get_clip/<int:clip_id>', methods=['GET', 'POST'])
def get_clip(clip_id):
    clip_meta = ClipMetadata.query.get(int(clip_id))
    
    if clip_meta:
        return clip_manager.get_clip(clip_meta)
    else:
        return jsonify(error_message='metadata not found'), 404        


@app.route('/add_clip', methods=['POST'])
def add_clip():
    required_params = ('stream_id', 'start_time', 'stop_time', 'container_format')
    not_provided = [key for key in required_params if key not in request.form]
    if not_provided:
        return jsonify(error_message='params required: {0}'.format(', '.join(not_provided))), 402

    stream_id = int(request.form['stream_id'])
    start_time = float(request.form['start_time'])
    stop_time = float(request.form['stop_time'])
    container_format = request.form['container_format']
    
    if 'data' not in request.files:
        return jsonify(error_message='No file attached'), 402
        
    clip_data = request.files['data']
        
    clip_meta = ClipMetadata(stream_id, start_time, stop_time, container_format)
    
    try:
        db_session.add(clip_meta)
        db_session.commit()
    except:
        db_session.rollback()
        get_logger().error("Can not write clip metadata. stream id = %d", stream_id)
        return jsonify(error_message='Internal error occured'), 500
    
    
    if not clip_manager.write_clip(clip_meta, clip_data) :
        db_session.delete(clip_meta)
        db_session.commit()
        get_logger().error("Can not write clip. clip id = %d", clip_meta.id)
        return jsonify(error_message='Internal error occured'), 500
    
    get_logger().info("Clip id=%d added to storage", clip_meta.id)

    result = { 'clip_id' : clip_meta.id }
    return jsonify(**result)


@app.route('/teststorage/add/<int:stream_id>/<int:start_time>', methods=['GET', 'POST'])
def testadd(stream_id, start_time):
    i = start_time - 2
    cf = 'mp4'
    cl = ClipMetadata(stream_id, i, i+17, cf)
    db_session.add(cl)
    
    i+=17
    db_session.add(ClipMetadata(stream_id, i, i+17, cf))
    i+=17
    db_session.add(ClipMetadata(stream_id, i, i+17, cf))
    i+=17+50
    db_session.add(ClipMetadata(stream_id, i, i+17, cf))
    i+=17+50
    db_session.add(ClipMetadata(stream_id, i, i+17, cf))
    i+=17
    db_session.add(ClipMetadata(stream_id, i, i+17, cf))
    
    db_session.commit()
    
    return jsonify(message='ok' + str(stream_id))

@app.route('/hello')
def hello():
    return 'pee-ba-la pa-ba-la poo!'

if __name__ == '__main__':
    app.run()
