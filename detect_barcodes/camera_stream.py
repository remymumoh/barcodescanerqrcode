import os

import cv2
import numpy as np
from pyzbar.pyzbar import decode


class CameraStream:
    used_codes = []
    def __init__(self):
        self.camera = cv2.VideoCapture(int(0))


    def get_frames(self):
        used_codes = self.used_codes
        while True:
            # Capture frame-by-frame
            success, frame = self.camera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)

                # Add text on top of the barcode if there is a barcode in the stream using opencv
                # convert camera frame to numpy array
                color_image = np.asanyarray(frame)


                # decode numpy array to check if there is a barcode in color_image
                if decode(color_image):
                    for code in decode(color_image):
                        if code.data.decode('utf-8') not in used_codes:
                            print('Approved. You can enter!')
                            print(code.data.decode('utf-8'))
                            used_codes.append(code.data.decode('utf-8'))
                        elif code.data.decode('utf-8') in used_codes:
                            print('Sorry, this code has been already used!')
                        else:
                            pass
                        cv2.imshow('Testing-code-scan', frame)
                        cv2.waitKey(1)
                    for barcode in decode(color_image):
                        # barcode_data = barcode.data.decode('utf-8')
                        # print(barcode_data)
                        # if barcode data exists
                        if barcode.data.decode('utf-8') not in used_codes:
                            print('Approved, you can enter!')
                            print(barcode.data.decode('utf-8'))
                        elif barcode.data.decode('utf-8') in used_codes:
                            print('Sorry, this code has been already used!')
                            print(used_codes)
                        else:
                            pass

                        if barcode.data.decode('utf-8'):
                            pts = np.array([barcode.polygon], np.int32)
                            pts = pts.reshape((-1, 1, 2))
                            # draw polylines on the barcode
                            cv2.polylines(
                                img=color_image,
                                pts=[pts],
                                isClosed=True,
                                color=(0, 255, 0),
                                thickness=3
                            )
                            pts2 = barcode.rect
                            # put text on top of polylines
                            barcode_frame = cv2.putText(
                                img=color_image,
                                text=barcode.data.decode('utf-8'),
                                org=(pts2[0], pts2[1]),
                                fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                                fontScale=0.9,
                                color=(0, 0, 255),
                                thickness=2
                            )
                            # encode the new barcode_frame that has polylines and barcode data text
                            _, buffer_ = cv2.imencode('.jpg', barcode_frame)
                            # convert barcode_frame to bytes
                            barcode_frame = buffer_.tobytes()
                            # yield output stream with polylines and barcode data text
                            yield (b'--frame\r\n'
                                   b'Content-Type: image/jpeg\r\n\r\n' + barcode_frame + b'\r\n\r\n')
                # else, yield the normal camera stream
                else:
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        return used_codes
