import sys, ipaddress
from pathlib import Path
import yaml
from jinja2 import Template

INTENT = Path("devices.yml")
TEMPLATE = Path("template.j2")
OUT = Path("configs")

def load_intent():
 return yaml.safe_load(INTENT.read_text())

def validate(devices):
    errors, seen = [], {}
    for dev in devices:
        for intf in dev.get("interfaces", []):
            ip = intf["ip"]
            try:
                ipaddress.ip_address(ip)
            except ValueError:
                errors.append(f"{dev['name']} {intf['name']}: invalid IP {ip}")
                continue
            if ip in seen:
                errors.append(f"duplicate IP {ip} on {dev['name']} {intf['name']} and {seen[ip]}")
            else:
                seen[ip] = f"{dev['name']} {intf['name']}"
    return errors

def main():
    devices = load_intent()["devices"]
    errors = validate(devices)
    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(" -", e)
        sys.exit(1)

    tmpl = Template(TEMPLATE.read_text())
    OUT.mkdir(exist_ok=True)
    for dev in devices:
        cfg = tmpl.render(device=dev)
        (OUT / f"{dev['name']}.cfg").write_text(cfg)
        print(f"--- configs/{dev['name']}.cfg ---")
        print(cfg)
    print(f"OK - generated {len(devices)} device config(s)")

if __name__ == "__main__":
 main()
