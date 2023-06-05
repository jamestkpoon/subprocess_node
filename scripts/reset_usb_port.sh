#!/bin/bash

bind_usb() {
  echo "$1" >/sys/bus/usb/drivers/usb/bind
}

unbind_usb() {
  echo "$1" >/sys/bus/usb/drivers/usb/unbind
}

unbind_usb "$1"
sleep 1
bind_usb "$1"