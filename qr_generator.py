#!/usr/bin/python3
import qrcode
from PIL import Image
logo_file_name = 'img/logo.png'

data = "http//:resqr.tech/user/profile/fjfjflkasjdlkfjalksjdlkfjffjskdlajfkjhjgfhhgfhhhfhgfhgfghfghfghfppppppppppppppp"
qr_code = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H, border=1
)
qr_code.add_data(data)
qr_code.make()

# qr code image
qr_code_image = qr_code.make_image(fill_color = 'black', 
                    back_color = (255, 79, 0)).convert('RGB')

# logo image 
logo = Image.open(logo_file_name).resize((100,100))


logo_x_position = (qr_code_image.size[0] - logo.size[0]) // 2
logo_y_position = (qr_code_image.size[1] - logo.size[1]) // 2
logo_position = (logo_x_position, logo_y_position)

# insert logo image into qr code image
qr_code_image.paste(logo, logo_position)

# save QR code image
qr_code_image.save('test.png')

print('QR successful generated')