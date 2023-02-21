from flask import Flask, redirect, render_template, request
import os
from monitorcontrol import get_monitors

tv = ""
id = ""
ip = ""
key = ""

app = Flask(__name__)

if len(tv) > 0:
    try:
        import panasonic_viera
        rc = panasonic_viera.RemoteControl(tv)
        tv_ok = True
    except:
        tv_ok = False
else:
    tv_ok = False


if len(id) > 0 and len(ip)> 0 and len(key) > 0:
    try:
        import tinytuya
        d = tinytuya.OutletDevice(id, ip, key)
        d.set_version(3.3)
        outlet_status = d.status()
        outlet_status = outlet_status['dps']['1']
        outlet_ok = True
    except:
        outlet_ok = False

@app.route('/')
def main():
    if tv_ok == True:
        remote = True
    else:
        remote = False

    if outlet_ok == True:
        outlet_status = d.status()
        outlet_status = outlet_status['dps']['1']
        if outlet_status == True:
            outlet = 'on'
            return render_template('index.html', outlet=outlet, remote=remote)
        else:
            outlet = 'off'
            return render_template('index.html', remote=remote, outlet=outlet)
    else:
        return render_template('index.html')
    


@app.route('/display', methods=['POST', 'GET'])
def display():
    for monitor in get_monitors():
        with monitor:
            luminance = monitor.get_luminance()
            contrast = monitor.get_contrast()
            source = monitor.get_input_source()
            screen_status = str(monitor.get_power_mode())
            screen_status = screen_status.split('.')
            screen_status = screen_status[1]

    if request.method == "POST":
        set_luminance = request.form.get('set_luminance')
        set_luminance = int(set_luminance)
        set_contrast = request.form.get('set_contrast')
        set_contrast = int(set_contrast)
        for monitor in get_monitors():
            with monitor:
                if set_luminance != luminance:
                    luminance = monitor.set_luminance(set_luminance)
                    print(f'Changed luminance to {set_luminance}')
                if set_contrast != contrast:
                    contrast = monitor.set_contrast(set_contrast)
                    print(f'Changed contrast to {set_contrast}')
        return render_template('display.html', screen_status=screen_status, luminance=set_luminance, contrast=set_contrast)
    else:
        return render_template('display.html', screen_status=screen_status, luminance=luminance, contrast=contrast, source=source)


@app.route('/display/nightmode')
def nightmode():
    print(f'Nightmode')
    for monitor in get_monitors():
        with monitor:
            if monitor.get_luminance != 0:
                monitor.set_luminance(0)
                print(f'Zmieniono jasność na 0%')
            if monitor.get_contrast != 50:
                monitor.set_contrast(50)
                print(f'Zmieniono kontrast na 50%')
    return redirect('/display')


@app.route('/display/normal')
def normal():
    print(f'Normal mode')
    for monitor in get_monitors():
        with monitor:
            if monitor.get_luminance != 100:
                monitor.set_luminance(100)
                print(f'Zmieniono jasność na 100%')
            if monitor.get_contrast != 50:
                monitor.set_contrast(50)
                print(f'Zmieniono kontrast na 50%')
    return redirect('/display')


@app.route('/display/vga')
def vga():
    print(f'Changed input to VGA')
    for monitor in get_monitors():
        with monitor:
            monitor.set_input_source('ANALOG1')
    return redirect('/display')


@app.route('/display/dvi')
def dvi():
    print(f'Changed input to DVI')
    for monitor in get_monitors():
        with monitor:
            monitor.set_input_source('DVI1')

    return redirect('/display')


@app.route('/display/screen_off')
def off():
    print(f'Screen off')
    try:
        for monitor in get_monitors():
            with monitor:
                monitor.set_power_mode('off_soft')
        return redirect('/display')
    except:
        return redirect('/')


@app.route('/display/screen_on')
def on():
    print(f'Screen On')
    for monitor in get_monitors():
        with monitor:
            monitor.set_power_mode('on')
    return redirect('/display')


@app.route('/outlet_status')
def outlet():
    if outlet_ok == True:
        outlet_status = d.status()
        outlet_status = outlet_status['dps']['1']
        if outlet_status == True:
            return "ON"
        else:
            return "OFF"
    else:
        return "Outlet not configured properly"

@app.route('/outlet_toggle')
def outlet_toggle():

    outlet_status = d.status()
    outlet_status = outlet_status['dps']['1']
    if outlet_status == True:
        d.turn_off()
        return redirect('/')
    else:
        d.turn_on()
        return redirect('/')


@app.route('/tv_status')
def tv_status():
    print(f'Sprawdzenie statusu TV')
    a = rc.get_volume()
    if a == 0:
        rc.volume_up()
        b = rc.get_volume()
        rc.volume_down()
    elif a == 100:
        rc.volume_down()
        b = rc.get_volume()
        rc.volume_up()
    else:
        rc.volume_down()
        b = rc.get_volume()
        rc.volume_up()
    status = (a != b)
    if status == True:
        return f'Twój telewizor jest włączony'
    else:
        return f'Twój telewizor jest wyłączony'


@app.route('/remote', methods=['GET', 'POST'])
def remote():
    volume_now = rc.get_volume()
    if request.method == "POST":
        set_volume = request.form.get('set_volume')
        set_volume = int(set_volume)
        if volume_now != set_volume:
            print(set_volume)
            rc.set_volume(set_volume)
        return render_template('remote.html', volume_now=volume_now)
    else:
        return render_template('remote.html', volume_now=volume_now)


@app.route('/remote/button_power')
def power():
    rc.send_key(panasonic_viera.Keys.power)
    print('power')
    return redirect('/remote')


@app.route('/remote/button_aspect')
def aspect():
    rc.send_key(panasonic_viera.Keys.aspect)
    print('aspect')
    return redirect('/remote')


@app.route('/remote/button_tv')
def tv():
    rc.send_key(panasonic_viera.Keys.tv)
    print('input_tv')
    return redirect('/remote')


@app.route('/remote/button_input')
def input_key():
    rc.send_key(panasonic_viera.Keys.input_key)
    print('input_av')
    return redirect('/remote')


@app.route('/remote/button_menu')
def menu():
    rc.send_key(panasonic_viera.Keys.menu)
    print('menu')
    return redirect('/remote')


@app.route('/remote/button_text')
def text():
    rc.send_key(panasonic_viera.Keys.text)
    print('text')
    return redirect('/remote')


@app.route('/remote/button_subs')
def subtitles():
    rc.send_key(panasonic_viera.Keys.subtitles)
    print('subtitles')
    return redirect('/remote')


@app.route('/remote/button_apps')
def apps():
    rc.send_key(panasonic_viera.Keys.apps)
    print('apps')
    return redirect('/remote')


@app.route('/remote/button_info')
def info():
    rc.send_key(panasonic_viera.Keys.info)
    print('info')
    return redirect('/remote')


@app.route('/remote/button_exit')
def exit():
    rc.send_key(panasonic_viera.Keys.exit)
    print('exit')
    return redirect('/remote')


@app.route('/remote/button_netflix')
def netflix():
    rc.launch_app('0010000200000001')
    print('netflix')
    return redirect('/remote')


@app.route('/remote/button_home')
def home():
    rc.send_key(panasonic_viera.Keys.home)
    print('home')
    return redirect('/remote')


@app.route('/remote/button_guide')
def guide():
    print('guide')
    rc.launch_app('0387878700000003')
    return redirect('/remote')


@app.route('/remote/button_up')
def up():
    rc.send_key(panasonic_viera.Keys.up)
    print('up')
    return redirect('/remote')


@app.route('/remote/button_left')
def left():
    rc.send_key(panasonic_viera.Keys.left)
    print('left')
    return redirect('/remote')


@app.route('/remote/button_enter')
def enter():
    rc.send_key(panasonic_viera.Keys.enter)
    print('enter')
    return redirect('/remote')


@app.route('/remote/button_right')
def right():
    rc.send_key(panasonic_viera.Keys.right)
    print('right')
    return redirect('/remote')


@app.route('/remote/button_down')
def down():
    rc.send_key(panasonic_viera.Keys.down)
    print('down')
    return redirect('/remote')


@app.route('/remote/button_option')
def option():
    rc.send_key(panasonic_viera.Keys.option)
    print('option')
    return redirect('/remote')


@app.route('/remote/button_back')
def back():
    rc.send_key(panasonic_viera.Keys.back)
    print('back')
    return redirect('/remote')


@app.route('/remote/button_red')
def red():
    rc.send_key(panasonic_viera.Keys.red)
    print('red')
    return redirect('/remote')


@app.route('/remote/button_green')
def green():
    rc.send_key(panasonic_viera.Keys.green)
    print('green')
    return redirect('/remote')


@app.route('/remote/button_yellow')
def yellow():
    rc.send_key(panasonic_viera.Keys.yellow)
    print('yellow')
    return redirect('/remote')


@app.route('/remote/button_blue')
def blue():
    rc.send_key(panasonic_viera.Keys.blue)
    print('blue')
    return redirect('/remote')


@app.route('/remote/button_vol_up')
def volume_up():
    rc.send_key(panasonic_viera.Keys.volume_up)
    print('volume_up')
    return redirect('/remote')


@app.route('/remote/button_vol_down')
def volume_down():
    rc.send_key(panasonic_viera.Keys.volume_down)
    print('volume_down')
    return redirect('/remote')


@app.route('/remote/button_mute')
def mute():
    rc.send_key(panasonic_viera.Keys.mute)
    print('mute')
    return redirect('/remote')


@app.route('/remote/button_ch_up')
def ch_up():
    rc.send_key(panasonic_viera.Keys.ch_up)
    print('ch_up')
    return redirect('/remote')


@app.route('/remote/button_ch_down')
def ch_down():
    rc.send_key(panasonic_viera.Keys.ch_down)
    print('ch_down')
    return redirect('/remote')


@app.route('/remote/button_1')
def num_1():
    rc.send_key(panasonic_viera.Keys.num_1)
    print('num_1')
    return redirect('/remote')


@app.route('/remote/button_2')
def num_2():
    rc.send_key(panasonic_viera.Keys.num_2)
    print('num_2')
    return redirect('/remote')


@app.route('/remote/button_3')
def num_3():
    rc.send_key(panasonic_viera.Keys.num_3)
    print('num_3')
    return redirect('/remote')


@app.route('/remote/button_4')
def num_4():
    rc.send_key(panasonic_viera.Keys.num_4)
    print('num_4')
    return redirect('/remote')


@app.route('/remote/button_5')
def num_5():
    rc.send_key(panasonic_viera.Keys.num_5)
    print('num_5')
    return redirect('/remote')


@app.route('/remote/button_6')
def num_6():
    rc.send_key(panasonic_viera.Keys.num_6)
    print('num_6')
    return redirect('/remote')


@app.route('/remote/button_7')
def num_7():
    rc.send_key(panasonic_viera.Keys.num_7)
    print('num_7')
    return redirect('/remote')


@app.route('/remote/button_8')
def num_8():
    rc.send_key(panasonic_viera.Keys.num_8)
    print('num_8')
    return redirect('/remote')


@app.route('/remote/button_9')
def num_9():
    rc.send_key(panasonic_viera.Keys.num_9)
    print('num_9')
    return redirect('/remote')


@app.route('/remote/button_ehelp')
def ehelp():
    rc.send_key(panasonic_viera.Keys.guide)
    print('ehelp')
    return redirect('/remote')


@app.route('/remote/button_0')
def num_0():
    rc.send_key(panasonic_viera.Keys.num_0)
    print('num_0')
    return redirect('/remote')


@app.route('/remote/button_last_view')
def last_view():
    rc.send_key(panasonic_viera.Keys.last_view)
    print('last_view')
    return redirect('/remote')


@app.route('/remote/button_rewind')
def rewind():
    rc.send_key(panasonic_viera.Keys.rewind)
    print('rewind')
    return redirect('/remote')


@app.route('/remote/button_play')
def play():
    rc.send_key(panasonic_viera.Keys.play)
    print('play')
    return redirect('/remote')


@app.route('/remote/button_forward')
def forward():
    rc.send_key(panasonic_viera.Keys.fast_forward)
    print('forward')
    return redirect('/remote')


@app.route('/remote/button_myapp')
def myapp():
    rc.launch_app('0387878700000130')
    print('stop')
    return redirect('/remote')


@app.route('/remote/button_stop')
def stop():
    rc.send_key(panasonic_viera.Keys.stop)
    print('stop')
    return redirect('/remote')


@app.route('/remote/cda')
def cda():
    print('cda')
    rc.launch_app('0076014507000001')
    return redirect('/remote')


@app.route('/remote/youtube')
def youtube():
    print('youtube')
    rc.launch_app('0070000200170001')
    return redirect('/remote')


@app.route('/remote/disney')
def disney():
    print('youtube')
    rc.launch_app('0070002900000002')
    return redirect('/remote')


###############################################################################


@app.route('/remote/button_next_track')
def next_track():
    print('next_track')
    rc.media_next_track()
    return redirect('/remote')


@app.route('/remote/button_previous_track')
def previous_track():
    print('previous_track')
    rc.media_previous_track()
    return redirect('/remote')


@app.route('/remote/button_media_pause')
def media_pause():
    print('media_pause')
    rc.media_pause()
    return redirect('/remote')

# @app.route('/remote/button_media_play')
# def media_play():
#     print('media_play')
#     rc.media_play()
#     return redirect('/remote')


###############################################################################


@app.route('/chiaki', methods=['POST', 'GET'])
def chiaki():
    if request.method == 'POST':

        psn = request.form.get('psn')

        from urllib.parse import urlparse, parse_qs, quote, urljoin
        import sys
        import requests
        import pprint
        import base64

        if sys.stdout.encoding.lower() == "ascii":
            import codecs
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)

        CLIENT_ID = "ba495a24-818c-472b-b12d-ff231c1b5745"
        CLIENT_SECRET = "mvaiZkRsAsI1IBkY"

        LOGIN_URL = "https://auth.api.sonyentertainmentnetwork.com/2.0/oauth/authorize?service_entity=urn:service-entity:psn&response_type=code&client_id={}&redirect_uri=https://remoteplay.dl.playstation.net/remoteplay/redirect&scope=psn:clientapp&request_locale=en_US&ui=pr&service_logo=ps&layout_type=popup&smcid=remoteplay&prompt=always&PlatformPrivacyWs1=minimal&".format(
            CLIENT_ID)
        TOKEN_URL = "https://auth.api.sonyentertainmentnetwork.com/2.0/oauth/token"

        code_url_s = psn
        code_url = urlparse(code_url_s)
        query = parse_qs(code_url.query)
        if "code" not in query or len(query["code"]) == 0 or len(query["code"][0]) == 0:
            print("☠️  URL did not contain code parameter")
            exit(1)
        code = query["code"][0]

        api_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
        body = "grant_type=authorization_code&code={}&redirect_uri=https://remoteplay.dl.playstation.net/remoteplay/redirect&".format(
            code)

        token_request = requests.post(TOKEN_URL,
                                      auth=api_auth,
                                      headers={
                                          "Content-Type": "application/x-www-form-urlencoded"},
                                      data=body.encode("ascii"))

        if token_request.status_code != 200:
            print("☠️  Request failed with code {}:\n{}".format(
                token_request.status_code, token_request.text))
            exit(1)

        token_json = token_request.json()
        if "access_token" not in token_json:
            print("☠️  \"access_token\" is missing in response JSON:\n{}".format(
                token_request.text))
            exit(1)
        token = token_json["access_token"]

        account_request = requests.get(
            TOKEN_URL + "/" + quote(token), auth=api_auth)

        if account_request.status_code != 200:
            print("☠️  Request failed with code {}:\n{}".format(
                account_request.status_code, account_request.text))
            exit(1)

        account_info = account_request.json()

        if "user_id" not in account_info:
            print("☠️  \"user_id\" is missing in response or not a string")
            exit(1)

        user_id = int(account_info["user_id"])
        user_id_base64 = base64.b64encode(
            user_id.to_bytes(8, "little")).decode()
            

        print(user_id_base64)
        for k, v in account_info.items():
            print(k, " = ", v)
        return render_template('chiaki.html', user_id_base64=user_id_base64)

    else:
        return render_template('chiaki.html')


if __name__ == "__main__":
    os.system('title Server')
    os.system('cls')
    app.run(host='0.0.0.0', port=80)
