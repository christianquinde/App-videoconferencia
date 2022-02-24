#!/bin/sh
#
# A simple RTP server
#  sends the output of v4l2src as VP8 encoded RTP on port 6000, RTCP is sent on
#  port 6001. The destination is 127.0.0.1.
#  the video receiver RTCP reports are received on port 6005
#  sends the output of autoaudiosrc as alaw encoded RTP on port 6002, RTCP is sent on
#  port 6003. The destination is 127.0.0.1.
#  the receiver RTCP reports are received on port 6007
#
#  .-------.    .-------.    .-------.      .----------.     .-------.
#  |v4lssrc|    | vp8enc|    | vp8pay|      | rtpbin   |     |udpsink|  RTP
#  |      src->sink    src->sink    src->send_rtp send_rtp->sink     | port=6000
#  '-------'    '-------'    '-------'      |          |     '-------'
#                                           |          |
#                                           |          |     .-------.
#                                           |          |     |udpsink|  RTCP
#                                           |    send_rtcp->sink     | port=6001
#                            .-------.      |          |     '-------' sync=false
#                 RTCP       |udpsrc |      |          |               async=false
#               port=6005    |     src->recv_rtcp      |
#                            '-------'      |          |
#                                           |          |
# .--------.    .-------.    .-------.      |          |     .-------.
# |audiosrc|    |alawenc|    |pcmapay|      | rtpbin   |     |udpsink|  RTP
# |       src->sink    src->sink    src->send_rtp send_rtp->sink     | port=6002
# '--------'    '-------'    '-------'      |          |     '-------'
#                                           |          |
#                                           |          |     .-------.
#                                           |          |     |udpsink|  RTCP
#                                           |    send_rtcp->sink     | port=6003
#                            .-------.      |          |     '-------' sync=false
#                 RTCP       |udpsrc |      |          |               async=false
#               port=6007    |     src->recv_rtcp      |
#                            '-------'      '----------'
#
# ideally we should transport the properties on the RTP udpsink pads to the
# receiver in order to transmit the SPS and PPS earlier.

# change this to send the RTP data and RTCP to another host
#DEST=10.8.0.2
DEST=$1
rate=$2
# tuning parameters to make the sender send the streams out of sync. Can be used
# ot test the client RTCP synchronisation.
#VOFFSET=900000000
VOFFSET=0
AOFFSET=0

# VP8 encode from the source
VELEM="v4l2src device=/dev/video0"
#VELEM="videotestsrc is-live=1"
VCAPS="video/x-raw,width=352,height=288,framerate=25/1"
VSOURCE="$VELEM ! queue ! videorate ! videoconvert ! videoscale ! $VCAPS"
#VENC="vp8enc target-bitrate=360000 keyframe-max-dist=30 cpu-used=2 deadline=1 ! rtpvp8pay"
VENC="vp8enc target-bitrate=$rate keyframe-max-dist=30 cpu-used=2 deadline=1 ! rtpvp8pay"

VRTPSINK="udpsink port=6000 host=$DEST ts-offset=$VOFFSET name=vrtpsink"
VRTCPSINK="udpsink port=6001 host=$DEST sync=false async=false name=vrtcpsink"
VRTCPSRC="udpsrc port=6005 name=vrtpsrc"

# PCMA encode from the source
AELEM="autoaudiosrc"
#AELEM="audiotestsrc is-live=1"
#AELEM="alsasrc device=hw:0"
ASOURCE="$AELEM ! queue ! audioresample ! audioconvert"
AENC="alawenc ! rtppcmapay"

ARTPSINK="udpsink port=6002 host=$DEST ts-offset=$AOFFSET name=artpsink"
ARTCPSINK="udpsink port=6003 host=$DEST sync=false async=false name=artcpsink"
ARTCPSRC="udpsrc port=6007 name=artpsrc"

gst-launch-1.0 -t rtpbin name=rtpbin \
    $VSOURCE ! $VENC ! rtpbin.send_rtp_sink_0                                             \
        rtpbin.send_rtp_src_0 ! $VRTPSINK                                                 \
        rtpbin.send_rtcp_src_0 ! $VRTCPSINK                                               \
      $VRTCPSRC ! rtpbin.recv_rtcp_sink_0                                                 \
    $ASOURCE ! $AENC ! rtpbin.send_rtp_sink_1                                             \
        rtpbin.send_rtp_src_1 ! $ARTPSINK                                                 \
        rtpbin.send_rtcp_src_1 ! $ARTCPSINK                                               \
      $ARTCPSRC ! rtpbin.recv_rtcp_sink_1
