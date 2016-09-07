import re
import shlex
from subprocess import check_output

class Xrandr(object):
    """Useful bindings for the xrandr command with some output parsing."""
    @staticmethod
    def _run_xrandr(options=''):
        """The whole output of an xrandr command (with given options) as a list
        of lines."""
        command = 'xrandr ' + options
        return check_output(shlex.split(command)).decode().splitlines()

    @staticmethod
    def modes(output):
        """A list of modes for the given output."""
        modes = []
        capture = False
        for line in Xrandr._run_xrandr():
            if line.startswith(output + ' '):
                capture = True
            elif capture and line.startswith(' '):
                modes.append(line.split()[0])
            elif not line.startswith(' '):
                capture = False
        return modes

    @staticmethod
    def outputs():
        """A list of xrandr outputs."""
        return [line for line in Xrandr._run_xrandr() if 'connected' in line]

    @staticmethod
    def add_virtual(resolution='1024x768'):
        """Add a virtual screen to the most recent disconnected VIRTUAL output
        with the given resolution."""
        valid_outputs = [output for output in Xrandr.outputs()
                         if re.match('VIRTUAL.*disconnected', output)]
        if not valid_outputs:
            raise ValueError('No valid output to add virtual screen to')

        name = valid_outputs.pop().split()[0]
        command = '--addmode {output} {resolution}'.format(
            output=name, resolution=resolution)
        Xrandr._run_xrandr(command)
        return name

    @staticmethod
    def rm_virtual(name):
        """Remove a screen (and all of its modes) with the given name."""
        Xrandr._run_xrandr('--output {name} --off'.format(name=name))
        for mode in Xrandr.modes(name):
            command = '--delmode {name} {mode}'.format(name=name, mode=mode)
            Xrandr._run_xrandr(command)

    @staticmethod
    def resolution(name, format_='{w}x{h}+{x}+{y}'):
        """Get the current resolution of the output name with the given
        format_. (format is w=width, h=height, x=xoffset, y=yoffset)"""
        regex = r'(?P<w>[0-9]*)x(?P<h>[0-9]*)\+(?P<x>[0-9]*)\+(?P<y>[0-9]*)'
        for line in Xrandr.outputs():
            if line.startswith(name + ' '):
                info = re.search(regex, line).groupdict()
                return format_.format(**info)
