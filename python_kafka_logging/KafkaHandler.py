from kafka.producer import KafkaProducer
import logging


class KafkaLoggingHandler(logging.Handler):

    def __init__(self, hosts_list, topic, **kwargs):
        logging.Handler.__init__(self)

        self.kafka_topic_name = topic
        self.producer = KafkaProducer(bootstrap_servers=hosts_list)

    def emit(self, record):
        # drop kafka logging to avoid infinite recursion
        if record.name == 'kafka':
            return
        try:
            # use default formatting
            msg = self.format(record)
            msg = str.encode(msg)

            self.producer.send(self.kafka_topic_name, msg)
            self.producer.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def close(self):
        if self.producer is not None:
            self.producer.close()
        logging.Handler.close(self)
