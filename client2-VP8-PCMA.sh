#!/bin/sh
#
# A simple RTP receiver
#
#  receives H264 encoded RTP video on port 6000, RTCP is received on  port 6001.
#  the receiver RTCP reports are sent to port 6005
#  receives alaw encoded RTP audio on port 6002, RTCP is received on  port 6003.
#  the receiver RTCP reports are sent to port 6007
#
#             .-------.      .----------.     .---------.   .-------.   .-----------.
#  RTP        |udpsrc |      | rtpbin   |     |h264depay|   |h264dec|   |xvimagesink|
#  port=6000  |      src->recv_rtp recv_rtp->sink     src->sink   src->sink         |
#             '-------'      |          |     '---------'   '-------'   '-----------'
#                            |          |
#                            |          |     .-------.
#                            |          |     |udpsink|  RTCP
#                            |    send_rtcp->sink     | port=6005
#             .-------.      |          |     '-------' sync=false
#  RTCP       |udpsrc |      |          |               async=false
#  port=6001  |     src->recv_rtcp      |
#             '-------'      |          |
#                            |          |
#             .-------.      |          |     .---------.   .-------.   .-------------.
#  RTP        |udpsrc |      | rtpbin   |     |pcmadepay|   |alawdec|   |autoaudiosink|
#  port=6002  |      src->recv_rtp recv_rtp->sink     src->sink   src->sink           |
#             '-------'      |          |     '---------'   '-------'   '-------------'
#                            |          |
#                            |          |     .-------.
#                            |          |     |udpsink|  RTCP
#                            |    send_rtcp->sink     | port=6007
#             .-------.      |          |     '-------' sync=false
#  RTCP       |udpsrc |      |          |               async=false
#  port=6003  |     src->recv_rtcp      |
#             '-------'      '----------'

# the destination machine to send RTCP to. This is the address of the sender and
# is used to send back the RTCP reports of this receiver. If the data is sent
# from another machine, change this address.
#DEST=127.0.0.1
DEST=$1
# this adjusts the latency in the receiver
LATENCY=200

# the caps of the sender RTP stream. This is usually negotiated out of band with
# SDP or RTSP. normally these caps will also include SPS and PPS but we don't
# have a mechanism to get this from the sender with a -launch line.
VIDEO_CAPS="application/x-rtp,media=(string)video,clock-rate=(int)90000,encoding-name=(string)VP8"
AUDIO_CAPS="application/x-rtp,media=(string)audio,clock-rate=(int)8000,encoding-name=(string)PCMA"

VIDEO_DEC="rtpvp8depay ! avdec_vp8"
AUDIO_DEC="rtppcmadepay ! alawdec"

VIDEO_SINK="videoconvert ! autovideosink"
AUDIO_SINK="audioresample ! audioconvert ! autoaudiosink"

gst-launch-1.0 -t rtpbin name=rtpbin latency=$LATENCY                                  \
     udpsrc caps=$VIDEO_CAPS port=6000 ! rtpbin.recv_rtp_sink_0                       \
       rtpbin. ! $VIDEO_DEC ! $VIDEO_SINK                                             \
     udpsrc port=6001 ! rtpbin.recv_rtcp_sink_0                                       \
         rtpbin.send_rtcp_src_0 ! udpsink port=6005 host=$DEST sync=false async=false \
     udpsrc caps=$AUDIO_CAPS port=6002 ! rtpbin.recv_rtp_sink_1                       \
       rtpbin. ! $AUDIO_DEC ! $AUDIO_SINK                                             \
     udpsrc port=6003 ! rtpbin.recv_rtcp_sink_1                                       \
         rtpbin.send_rtcp_src_1 ! udpsink port=6007 host=$DEST sync=false async=false
