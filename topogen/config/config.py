from math import log2, log10
from os import path

from topogen.utils.function import get_yaml_data

dir_path = path.dirname(path.realpath(__file__))
channel_config = get_yaml_data(path.join(dir_path, 'channel_config.yaml'))

bandwidth           = channel_config['bandwidth']['value']
noise_coefficient   = channel_config['noise_coefficient']['value']
tx_power            = channel_config['tx_power']['value']
carrier_frequency   = channel_config['carrier_frequency']['value']
interference        = channel_config['interference']['value']

dbm_to_watt     = lambda dbm: 10 ** (dbm / 10) / 1000 # dbm -> watt
path_loss       = lambda dist, fc: 32.4 + (21 * log10(dist)) + (20 * log10(fc)) # db
rx_power        = lambda dist: tx_power - path_loss(dist, carrier_frequency) + 40 - 7 # dbm
rx_power_watt   = lambda dist: dbm_to_watt(rx_power(dist)) # watt
noise_watt      = dbm_to_watt(noise_coefficient) * bandwidth # watt

sinr    = lambda dist: rx_power_watt(dist) / (noise_watt + interference) # ratio
snr     = lambda dist: rx_power_watt(dist) - noise_watt # ratio

shanon_capacity = lambda dist: bandwidth * log2(1 + sinr(dist)) # bps

DATA_RATE_BPS_FORMULA = lambda dist: shanon_capacity(dist) # bps