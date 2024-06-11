import subprocess


class ServiceManager:
    def get_services(self):
        command = ['systemctl', 'list-units', '--type=service', '--all', '--no-pager']
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        services = []
        lines = result.stdout.splitlines()
        for line in lines[1:]:
            parts = line.split(maxsplit=4)
            if len(parts) < 5:
                continue
            service_name = parts[0]
            status = parts[3]
            description = parts[4] if len(parts) > 4 else ""
            services.append((service_name, description, status))
        return services
