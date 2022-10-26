#!/usr/bin/python3

import qrcode
from PIL import Image


def create_qr(data='', design="orange"):
    if design == "orange":
        logo_file_name = 'static/logoOrange.png'
    elif design == "blue":
        logo_file_name = 'static/logoBlue.png'
    else:
        logo_file_name = 'static/logoGreen.png'


    qr_code = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H, border=1
    )
    qr_code.add_data('http://resqr.tech/profile/' + data)
    qr_code.make()

    # qr code image
    if design == "orange":
        qr_code_image = qr_code.make_image(fill_color='black',
                                           back_color=(255, 79, 0)).convert('RGB')
    elif design == "green":
        qr_code_image = qr_code.make_image(fill_color='black',
                                           back_color=(0, 255, 0)).convert('RGB')
    else:
        qr_code_image = qr_code.make_image(fill_color='white',
                                           back_color=(0, 0, 255)).convert('RGB')

    # logo image
    logo = Image.open(logo_file_name).resize((100, 100))

    logo_x_position = (qr_code_image.size[0] - logo.size[0]) // 2
    logo_y_position = (qr_code_image.size[1] - logo.size[1]) // 2
    logo_position = (logo_x_position, logo_y_position)

    # insert logo image into qr code image
    qr_code_image.paste(logo, logo_position)

    # save QR code image
    img_name = data + '.png'
    qr_code_image.save('static/{}'.format(img_name), 'PNG')

    print('QR successful generated')
