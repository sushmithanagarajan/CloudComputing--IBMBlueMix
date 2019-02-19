import urllib2
# from PIL import Image
import pyDes
# import PIL.Image
# import base64
import hashlib
from flask import Flask, render_template, request

# from Crypto.Cipher import AES
import swiftclient
import keystoneclient
import os

# from simple_aes_cipher import cipher
f1 = ''
totalsize = ''
size = ''
auth_url = 'https://identity.open.softlayer.com' + '/v3'
projectId = 'a5dd8dc014dd4be2b1433'
region = 'dallas'
userId = 'c2b5'
password = ''
container_name = 'SushContainer'
conn = swiftclient.Connection(key=password,
                              authurl=auth_url,
                              auth_version='3',
                              os_options={"project_id": projectId,
                                          "user_id": userId,
                                          "region_name": region})
# dpath = 'C:/Users/get-started-python-master/download'
dpath = ''
folder = 'C:/Users/Sushmitha Nagarajan/Desktop/CloudComputing'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'jpg', 'jpeg', 'gif', 'xml'])

k = pyDes.des("DESCRYPT", pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1])]

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = folder

dic = {}


@app.route('/', methods=['POST', 'GET'])
def main_page():
    res = ""
    file_download = ""
    if request.method == 'POST':
        if request.form['submit'] == 'Upload':
            global f1
            f1 = request.files['file_upload']
            key = request.form['key']
            # print 'a'
            upload(f1.filename)

        elif request.form['submit'] == 'Download':
            f1 = request.form['file_download']
            dkey = request.form['dkey']
            # print f1
            download(f1)


        elif request.form['submit'] == 'List':
            # print 'list'
            res = list()


        elif request.form['submit'] == 'Remove':
            size = request.form['fsize']
            remove(size)

    return render_template('index1.html', res=res)


def upload(filename):
    # fname, ext = os.path.splitext(filename)
    # if ext == ".txt":
    global f1
    fl = request.files['file_upload']
    filename = str(f1.filename)
    data = fl.read()
    #  content=encrypt_val(data,key)
    # print 'data'+ data
    # contents = cipher.encrypt(data,ukey)
    no = checksum(data)
    # print'hi'+ no
    text = data + '$$$$$$$$$' + no
    # contents = k.encrypt(text)
    contents = text
    dic[f1.filename] = no
    # print 'hello'+ dic[f1.filename]
    # print contents
    fname, ext = os.path.splitext(f1.filename)
    # print fname
    # if ext == ".txt":
    global size
    if size <= '10000':

        conn.put_object('SushContainer', f1.filename, contents, content_type='text/plain')
    else:
        # This has to be reviewed and removed
        conn.put_object('SushContainer', f1.filename, contents, content_type='text/plain')
    # print filename
    fl.close()


def checksum(data):
    global f1
    md5 = hashlib.md5()
    md5.update(data)
    return md5.hexdigest()


def list():
    list = ""
    for container in conn.get_account()[1]:
        for data in conn.get_container(container['name'])[1]:
            list += (
            '\r\nobject: {0} size: {1} date: {2}\r\n'.format(data['name'], data['bytes'], data['last_modified']))
          
    return list


def download(filename):
    fname, ext = os.path.splitext(filename)
    for container in conn.get_account()[1]:
        # print "Container ",container
        for data1 in conn.get_container(container['name'])[1]:
            # print filename
            # print data1['name']
            if filename == data1['name']:
                # print "in if"
                try:
                    fobj = conn.get_object(container['name'], filename)
                    # print fobj
                    # contents = k.decrypt(dfile)
                    # print 'a'
                    # if ext == '.txt':
                    # open()
                    with open(filename, 'wb') as fw:
                        data = str(fobj)
                        fw.write(data)
                        fw.close()


                except urllib2.HTTPError as err:
                    if err.code == 404:
                        continue
                # print 'Filename download is'
                # print filename
                return render_template('index1.html', file_download=filename)


def remove(size):
    for container in conn.get_account()[1]:
        for data in conn.get_container(container['name'])[1]:
            print data['bytes']
            if int(data['bytes']) < int(size):
                conn.delete_object(container['name'], data['name'])


port = int(os.getenv('VCAP_APP_PORT', 8080))
if __name__ == '__main__':
    app.run(debug=True, port=5001)
    # For Local Runn
    # For Local Runn
    # app.run(debug=True,host = '0.0.0.0', port=port)

