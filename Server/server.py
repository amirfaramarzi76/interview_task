import zmq
import json
import subprocess
from django.conf import settings

class proccessCommand:
    def __init__(self, ):
        self.allowed_os_commands = ["ping", "dir"]
    def os_command(self,command_name,parameters):
        if command_name not in self.allowed_os_commands:
            return {"status": "error", "message": "Command not allowed"}
        try:
            result = subprocess.run(
                [command_name] + parameters,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return {"status": "success", "result": result.stdout.strip()}
            else:
                return {"status": "error", "message": result.stderr.strip()}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def math_command(self, expression):
        try:
            result = eval(expression)
            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def process(self, command):
        command_type = command.get("command_type")
        if command_type == "os":
            return self.os_command(command.get("command_name"), command.get("parameters", []))
        elif command_type == "compute":
            return self.math_command(command.get("expression"))
        else:
            return {"status": "error", "message": "Invalid command type"}

def start_server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://127.0.0.1:{settings.ZMQ_PORT}")

    print("Server is running...")
    processor = proccessCommand()

    while True:
        try:
            message = socket.recv_string()
            try:
                command = json.loads(message)
            except json.JSONDecodeError:
                socket.send_json({"status": "error", "message": "Invalid JSON format"})
                continue
            response = processor.process(command)
            socket.send_json(response)

        except Exception as e:
            socket.send_json({"status": "error", "message": str(e)})

if __name__ == "__main__":
    start_server()