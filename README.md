# Battery Charge Notifier

## Task

It's recommended do not overcharge and do not downcharge Li-ion battery on notebooks to prolongate battery lifetime

Some vendors provide hardware and software feature to stop battery charging when percentage is greater than some threshold

This solution for Linux OS those who haven't that feature

It's only notifies when battery level lower than and upper than any threshold and shows a recommendation to connect or disconnect out AC adapter

## Requirements

* python3
* `upower` command line utility
* PyGObject module

## Configure

* edit `battery_charge_notifier.conf`

## Run

* run `python3 -m battery_charge_notifier` from path where `battery_charge_notifier` is located

## TODO's

- [ ] implement as daemon according to [pep-3143](https://www.python.org/dev/peps/pep-3143/)
- [ ] make crossplatform
- [ ] add tests
- [ ] add run script
- [ ] add installation script
- [ ] add custom icons for notifications
