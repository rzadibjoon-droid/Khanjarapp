"""
═══════════════════════════════════════════════════════════════
🔥 KHANJAR SUPREME V5.0 — ANDROID APK
═══════════════════════════════════════════════════════════════
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.utils import platform
from kivy.properties import StringProperty

from scanner import KhanjarSupremeV5
import threading
import json
from datetime import datetime

if platform == 'android':
    from jnius import autoclass, cast
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.INTERNET,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.READ_EXTERNAL_STORAGE,
        Permission.VIBRATE
    ])

    PythonService = autoclass('org.kivy.android.PythonService')
    NotificationBuilder = autoclass('android.app.Notification$Builder')
    NotificationManager = autoclass('android.app.NotificationManager')
    Context = autoclass('android.content.Context')
    PendingIntent = autoclass('android.app.PendingIntent')
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')
    RingtoneManager = autoclass('android.media.RingtoneManager')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Color = autoclass('android.graphics.Color')
    NotificationCompat = autoclass('androidx.core.app.NotificationCompat')
    BigTextStyle = autoclass('android.app.Notification$BigTextStyle')


class KhanjarApp(App):
    status_text = StringProperty("⏸ آماده اسکن")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scanner = None
        self.scanning = False
        self.scan_thread = None
        self.scan_interval = 60  # 1 minute

    def build(self):
        self.title = "🔥 Khanjar Supreme V5.0"
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        header = Label(
            text="🔥 KHANJAR SUPREME V5.0\n💎 Ultimate Trading Scanner",
            size_hint_y=0.15,
            font_size='20sp',
            bold=True
        )
        layout.add_widget(header)
        
        self.status_label = Label(
            text=self.status_text,
            size_hint_y=0.1,
            font_size='16sp'
        )
        layout.add_widget(self.status_label)
        
        scroll = ScrollView(size_hint=(1, 0.6))
        self.results_label = Label(
            text="🎯 نتایج اسکن اینجا نمایش داده می‌شود...",
            size_hint_y=None,
            font_size='14sp',
            markup=True
        )
        self.results_label.bind(texture_size=self.results_label.setter('size'))
        scroll.add_widget(self.results_label)
        layout.add_widget(scroll)
        
        btn_layout = BoxLayout(size_hint_y=0.15, spacing=10)
        
        self.start_btn = Button(
            text="▶️ شروع اسکن",
            background_color=(0, 0.8, 0, 1),
            font_size='18sp',
            bold=True
        )
        self.start_btn.bind(on_press=self.start_scanning)
        btn_layout.add_widget(self.start_btn)
        
        self.stop_btn = Button(
            text="⏹ توقف",
            background_color=(0.8, 0, 0, 1),
            font_size='18sp',
            bold=True,
            disabled=True
        )
        self.stop_btn.bind(on_press=self.stop_scanning)
        btn_layout.add_widget(self.stop_btn)
        
        layout.add_widget(btn_layout)
        
        return layout

    def start_scanning(self, instance):
        if self.scanning:
            return
            
        self.scanning = True
        self.start_btn.disabled = True
        self.stop_btn.disabled = False
        self.status_text = "🔄 در حال اسکن..."
        self.status_label.text = self.status_text
        
        self.scan_thread = threading.Thread(target=self.scan_loop, daemon=True)
        self.scan_thread.start()
        
        if platform == 'android':
            self.start_service()

    def stop_scanning(self, instance):
        self.scanning = False
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        self.status_text = "⏸ توقف اسکن"
        self.status_label.text = self.status_text
        
        if platform == 'android':
            self.stop_service()

    def scan_loop(self):
        while self.scanning:
            try:
                self.perform_scan()
            except Exception as e:
                Clock.schedule_once(lambda dt: self.update_results(f"❌ خطا: {str(e)}"))
            
            for _ in range(self.scan_interval):
                if not self.scanning:
                    break
                import time
                time.sleep(1)

    def perform_scan(self):
        try:
            self.scanner = KhanjarSupremeV5()
            results = self.scanner.run_for_app()
            
            Clock.schedule_once(lambda dt: self.display_results(results))
            
            if results and len(results) > 0:
                self.send_notification(results[0])
                
        except Exception as e:
            Clock.schedule_once(lambda dt: self.update_results(f"❌ خطا در اسکن: {str(e)}"))

    def display_results(self, results):
        if not results:
            text = f"[color=ff6b6b]❌ سیگنالی یافت نشد[/color]\n"
            text += f"⏰ زمان: {datetime.now().strftime('%H:%M:%S')}\n"
            text += f"🔄 اسکن بعدی: {self.scan_interval} ثانیه دیگر"
            self.results_label.text = text
            return
        
        text = f"[color=4ecdc4]✅ {len(results)} سیگنال یافت شد![/color]\n\n"
        
        for i, sig in enumerate(results[:3], 1):
            emoji = "🟢" if sig['dir'] == "LONG" else "🔴"
            text += f"{emoji} [b]#{i} — {sig['sym']}[/b]\n"
            text += f"   📊 {sig['dir']} | Entry: {sig['entry']}\n"
            text += f"   🎯 TP1: {sig['tp1']} | TP2: {sig['tp2']}\n"
            text += f"   🛡 SL: {sig['sl']} | R:R={sig['rr']}\n"
            text += f"   ⚡ LEV: {sig['lev']['lev']}x | Score: {sig['score']}\n\n"
        
        text += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self.results_label.text = text

    def update_results(self, message):
        self.results_label.text = message

    def send_notification(self, signal):
        if platform != 'android':
            return
            
        try:
            context = PythonActivity.mActivity
            
            channel_id = "khanjar_signals"
            
            title = f"🔥 سیگنال {signal['dir']} - {signal['sym']}"
            message = f"Entry: {signal['entry']} | SL: {signal['sl']}\nTP1: {signal['tp1']} | R:R={signal['rr']}"
            
            sound_uri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION)
            
            builder = NotificationCompat.Builder(context, channel_id)
            builder.setContentTitle(title)
            builder.setContentText(message)
            builder.setSmallIcon(context.getApplicationInfo().icon)
            builder.setAutoCancel(True)
            builder.setSound(sound_uri)
            builder.setPriority(NotificationCompat.PRIORITY_HIGH)
            builder.setVibrate([0, 500, 200, 500])
            
            if signal['dir'] == "LONG":
                builder.setColor(Color.GREEN)
            else:
                builder.setColor(Color.RED)
            
            big_text = BigTextStyle()
            big_text.setBigContentTitle(title)
            big_text.bigText(message)
            builder.setStyle(big_text)
            
            notification_manager = context.getSystemService(Context.NOTIFICATION_SERVICE)
            notification_manager.notify(1001, builder.build())
            
        except Exception as e:
            print(f"Notification error: {e}")

    def start_service(self):
        try:
            service = autoclass('org.kivy.android.PythonService')
            service.start('Khanjar Scanner Running', '')
        except:
            pass

    def stop_service(self):
        try:
            service = autoclass('org.kivy.android.PythonService')
            service.stop()
        except:
            pass


if __name__ == '__main__':
    KhanjarApp().run()
