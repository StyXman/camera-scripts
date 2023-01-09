#! /usr/bin/env python3

import argparse

import gphoto2

# A3: 297x420mm, center 148.5x210


def init_camera():
    camera = gphoto2.check_result(gphoto2.gp_camera_new())
    print('Please connect and switch on your camera')
    while True:
        try:
            camera.init()
        except gphoto2.GPhoto2Error as ex:
            if ex.code == gphoto2.GP_ERROR_MODEL_NOT_FOUND:
                # no camera, try again in 2 seconds
                time.sleep(2)
                continue
            # some other error we can't handle here
            raise
        # operation completed successfully so exit loop
        break


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--camera', default='Nikon D7200')
    parser.add_argument('--lens', default='AF-S NIKKOR 18-140mm 3.5-5.6G')

    return parser.parse_args()


def snake_case(string):
    return string.replace(' ', '_')


def get_camera():
    # init_camera()
    print('Ready')
    camera = gphoto2.Camera()
    print('Initializing camera')
    camera.init()

    return camera


def empty_event_queue(camera):
    type, data = camera.wait_for_event(1)
    while type != gphoto2.GP_EVENT_TIMEOUT:
        print(f"""[{type}] {data}""")
        type, data = camera.wait_for_event(1)


def capture(camera, zoom, f_value):
    new_value = f"""f/{f_value}"""
    print(f"""Capturing {new_value}""")

    print('Getting Config')
    config = camera.get_config()
    config.get_child_by_name('actions').get_child_by_name('autofocusdrive').set_value(True)
    config.get_child_by_name('capturesettings').get_child_by_name('exposurecompensation').set_value('0')

    config.get_child_by_name('capturesettings').get_child_by_name('f-number').set_value(new_value)
    print(f"""Setting config for {new_value}""")
    camera.set_config(config)

    config = camera.get_config()
    camera_value = config.get_child_by_name('capturesettings').get_child_by_name('f-number').get_value()
    if camera_value != new_value:
        print(f"""Camera didn't accept value, it's {camera_value}; skipping""")
        print()
        return

    dst = f"""{snake_case(opts.camera)}-{snake_case(opts.lens)}-{zoom}-f_{f_value}.jpg"""

    print('Capturing')
    src = camera.capture(gphoto2.GP_CAPTURE_IMAGE)
    print('Fetching')
    file = camera.file_get(src.folder, src.name, gphoto2.GP_FILE_TYPE_NORMAL)
    print('Saving')
    file.save(dst)
    print('Done.')
    empty_event_queue(camera)
    print()


def main(opts):
    f_values = [ '3.5', '3.8', '4', '4.2', '4.5', '4.8', '5', '5.3', '5.6', '6.3', '7.1', '8', '9', '10', '11' ]

    camera = get_camera()

    while True:
        zoom = input('Please enter the next zoom: ')
        if zoom == '':
            break

        for f_value in f_values:
            try:
                capture(camera, zoom, f_value)
            except gphoto2.GPhoto2Error as e:
                # gphoto2.GPhoto2Error: [-110] I/O in progress
                # print(f"""got {e.code}, [{e.args}], {dir(e)}""")
                print('Found an error, resetting the camera')
                print()
                # gphoto2.GPhoto2Error: [-53] Could not claim the USB device
                camera.exit()
                camera = get_camera()
                capture(camera, zoom, f_value)


if __name__ == '__main__':
    opts = parse_args()
    main(opts)
