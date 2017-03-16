from django import forms

class AddForm(forms.Form):
    service_name = forms.CharField(label='Service name', max_length=100, required=True)
    imagefile = forms.FileField(label='Image file', required=False)
    url = forms.CharField(label='Image URL', max_length=100, required=False)

    def is_valid(self):
        valid = super(AddForm, self).is_valid()
        if not valid:
            return False
        else:
            return 'url' in self.data or 'imagefile' in self.files

class PortForm(forms.Form):
    PORT_DIRECT_FIELD_PREFIX = 'port_direct_'
    PORT_PROXY_FIELD_PREFIX = 'port_proxy_'
    PORT_HOSTNAME_FIELD_PREFIX = 'port_hostname_'

    def get_direct_field_name(self, port_name):
        return self.PORT_DIRECT_FIELD_PREFIX + str(port_name)

    def get_proxy_field_name(self, port_name):
        return self.PORT_PROXY_FIELD_PREFIX + str(port_name)

    def get_hostname_field_name(self, port_name):
        return self.PORT_HOSTNAME_FIELD_PREFIX + str(port_name)

    def add_port(self, port_name, direct_port, proxy_port, hostname):
        direct_field = forms.IntegerField(label=port_name + ' directly to port',
                                          initial=direct_port,
                                          min_value=1,
                                          max_value=2**16-1,
                                          required=False)
        self.fields[self.get_direct_field_name(port_name)] = direct_field

        proxy_field = forms.IntegerField(label=port_name + ' via reverse proxy to port',
                                         initial=proxy_port,
                                         min_value=1,
                                         max_value=2**16-1,
                                         required=False)
        self.fields[self.get_proxy_field_name(port_name)] = proxy_field

        hostname_field = forms.CharField(label=port_name + ' hostname ',
                                         initial=hostname,
                                         max_length=100,
                                         required=False)
        self.fields[self.get_hostname_field_name(port_name)] = hostname_field

    def add_ports(self, port_map):
        print('add_ports/port_map', port_map)
        for port_name in sorted(port_map):
            port = port_map[port_name] or {}
            direct_port = port.get('direct_port', None)
            proxy_port = port.get('proxy_port', None)
            hostname = port.get('hostname', None)
            self.add_port(port_name, direct_port, proxy_port, hostname)
