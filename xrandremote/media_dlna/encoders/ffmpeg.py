from __future__ import unicode_literals

import logging

from pulseaudio_dlna.encoders.ffmpeg import (
    FFMpegMp3Encoder, FFMpegWavEncoder, FFMpegL16Encoder, FFMpegAacEncoder,
    FFMpegOggEncoder, FFMpegFlacEncoder, FFMpegOpusEncoder)

logger = logging.getLogger('xrandrremote.media_dlna.encoders.ffmpeg')

