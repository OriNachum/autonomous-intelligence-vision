import subprocess

def get_ethernet_ip():
    ip_command_output = subprocess.check_output(
        ["ip", "addr", "show", "eth0"],
    )
    ip_command_output_output_lines = ip_command_output.decode().split("\n")
    print(ip_command_output_output_lines[2])
    ip_address = (
        ip_command_output_output_lines[2].split()[1].split("/")[0]
    )
    
    return ip_address

if __name__ == "__main__":
    print("Testing get_current_ip")
    current_ip = get_ethernet_ip()
    print(f"Current ip is: {current_ip}")
