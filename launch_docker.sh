./x-docker run --gpus all --net=host -it --rm --privileged -v `pwd`:/root/pkgs/residual_shared_autonomy residual_shared_autonomy:latest bash
# sudo x-docker
# nvidia-docker -e NVIDIA_VISIBLE_DEVICES=all -e NVIDIA_DRIVER_CAPABILITIES=graphics -it -e DISPLAY=$NET_IP$DISPLAY_NO -e QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix:/tmp/.X11-unix
