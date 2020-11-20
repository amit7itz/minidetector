#! /usr/bin/env python3
import argparse
import threading
import logging

from scapy.all import sniff, Ether, IP
from .database import create_tables, Entity, create_session, drop_tables
from queue import Queue

packet_queue = Queue()


def on_packet(p):
    if Ether not in p or IP not in p:
        return
    packet_queue.put(p)


def process_data():
    packet_count = 0
    while packet := packet_queue.get():
        packet_count += 1
        if packet_count % 100 == 0:
            logging.info(f'Queue size: {packet_queue.qsize()}')
        mac = packet[Ether].src
        ip = packet[IP].src
        session = create_session()
        query = session.query(Entity).filter_by(mac=mac, ip=ip)
        if query.count() > 0:
            logging.debug(f'skipping packet {ip} {mac}')
            continue
        entity = Entity(mac=mac, ip=ip)
        session.add(entity)
        session.commit()
        logging.info(f'Added entity {entity}')
        session.close()


def main():
    parser = argparse.ArgumentParser(description='Minidetector is an example tool for detecting network identities and insert them into a postgres database')
    parser.add_argument("--clean", const=True, default=False, nargs='?', help="prune the existing data before starting")
    parser.add_argument("--debug", const=True, default=False, nargs='?', help="enable debug logging")
    args = parser.parse_args()
    logging.root.setLevel(logging.DEBUG if args.debug else logging.INFO)
    if args.clean:
        logging.debug('Dropping all tables')
        drop_tables()
    logging.debug('Creating all tables')
    create_tables()
    logging.debug('Starting sniffing thread')
    sniffing_thread = threading.Thread(target=lambda: sniff(prn=on_packet), daemon=True)
    sniffing_thread.start()
    logging.debug('Starting to process packets')
    process_data()


if __name__ == '__main__':
    main()
