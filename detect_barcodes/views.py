from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from .camera_stream import CameraStream


# Create your views here.
def camera_feed(request):
    stream = CameraStream()
    frames = stream.get_frames()
    return StreamingHttpResponse(frames, content_type='multipart/x-mixed-replace; boundary=frame')


def detect(request):
    stream = CameraStream()
    success, frame = stream.camera.read()
    if success:
        status = True
    else:
        status = False
    bar_codes = stream.used_codes
    print(bar_codes)
    html = render_to_string('detect_barcodes/detect.html', context={'bar_codes': bar_codes, 'cam_status': status})

    return HttpResponse(html)
    #return render(request, 'detect_barcodes/detect.html', context={'bar_codes': bar_codes, 'cam_status': status})
