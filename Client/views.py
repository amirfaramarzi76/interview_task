import zmq
import json
from django.shortcuts import render
from django.http import JsonResponse
from .forms import JSONFileUploadForm
from commons.errors import ErrorMessages
from django.conf import settings


def upload_json(request):
    if request.method == 'POST':
        form = JSONFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            json_file = request.FILES['json_file']
            try:
                command = json.load(json_file)
                context = zmq.Context()
                socket = context.socket(zmq.REQ)
                socket.connect(f"tcp://127.0.0.1:{settings.ZMQ_PORT}")
                socket.send_string(json.dumps(command))

                response = socket.recv_json()

                return JsonResponse(response)


            except json.JSONDecodeError:
                return JsonResponse(ErrorMessages.invalid_json_format())
            except zmq.ZMQError as zmq_error:
                return JsonResponse(ErrorMessages.zmq_error(str(zmq_error)))
            except Exception as e:
                return JsonResponse(ErrorMessages.unexpected_error(str(e)))
    else:
        form = JSONFileUploadForm()

    return render(request, 'Client/upload_json.html', {'form': form})
