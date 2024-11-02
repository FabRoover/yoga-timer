from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.utils import platform
from kivy.storage.jsonstore import JsonStore
from kivy.uix.popup import Popup
from kivy.core.audio import SoundLoader
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.checkbox import CheckBox
from flask import Flask
import threading
import os
import json
import random
from datetime import datetime, timedelta
import uuid

class DataManager:
    def __init__(self):
        self.store = JsonStore('yoga_data.json')
        self.poses = self.load_data('poses', [])
        self.sequences = self.load_data('sequences', [])
        self.statistics = self.load_data('statistics', {
            'total_sessions': 0,
            'total_time': 0,
            'pose_counts': {},
            'daily_stats': {}
        })
        self.current_sequence = None
        
    def load_data(self, key, default):
        try:
            if key in self.store:
                return self.store.get(key)['data']
        except:
            pass
        return default
        
    def save_data(self, key, data):
        self.store.put(key, data=data)
        
    def add_pose(self, name, duration=60, warning_time=10, repetitions=1):
        pose = {
            'id': str(uuid.uuid4()),
            'name': name,
            'duration': duration,
            'warning_time': warning_time,
            'repetitions': repetitions,
            'created_at': datetime.now().isoformat()
        }
        self.poses.append(pose)
        self.save_data('poses', self.poses)

class TimerScreen(BoxLayout):
    def __init__(self, data_manager, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        self.data_manager = data_manager
        self.current_time = 60
        self.timer_active = False
        self.poses_completed = []
        self.session_start_time = None
        
        # Main timer display
        self.pose_label = Label(
            text="Press Start to Begin",
            font_size='24sp',
            size_hint_y=0.3
        )
        self.timer_label = Label(
            text="60",
            font_size='48sp',
            size_hint_y=0.3
        )
        
        # Control buttons
        controls = BoxLayout(size_hint_y=0.2, spacing=10)
        self.start_button = Button(
            text='Start',
            on_press=self.toggle_timer,
            background_color=(0.2, 0.8, 0.2, 1)
        )
        self.randomize_button = Button(
            text='Randomize',
            on_press=self.randomize_pose,
            background_color=(0.2, 0.2, 0.8, 1)
        )
        
        controls.add_widget(self.start_button)
        controls.add_widget(self.randomize_button)
        
        # Timer settings
        settings = BoxLayout(size_hint_y=0.2, spacing=10)
        self.duration_input = TextInput(
            text='60',
            multiline=False,
            input_filter='int',
            size_hint_x=0.3
        )
        self.warning_input = TextInput(
            text='10',
            multiline=False,
            input_filter='int',
            size_hint_x=0.3
        )
        
        settings.add_widget(Label(text='Duration (s):'))
        settings.add_widget(self.duration_input)
        settings.add_widget(Label(text='Warning at:'))
        settings.add_widget(self.warning_input)
        
        # Add all elements to main layout
        self.add_widget(self.pose_label)
        self.add_widget(self.timer_label)
        self.add_widget(controls)
        self.add_widget(settings)
        
    def toggle_timer(self, instance):
        if not self.timer_active:
            self.start_timer()
        else:
            self.stop_timer()
            
    def start_timer(self):
        self.timer_active = True
        self.start_button.text = 'Stop'
        self.start_button.background_color = (0.8, 0.2, 0.2, 1)
        self.current_time = int(self.duration_input.text)
        Clock.schedule_interval(self.update_timer, 1)
        
        if not self.session_start_time:
            self.session_start_time = datetime.now()
        
        # Play start sound
        sound = SoundLoader.load('assets/start.wav')
        if sound:
            sound.play()
            
    def stop_timer(self):
        self.timer_active = False
        self.start_button.text = 'Start'
        self.start_button.background_color = (0.2, 0.8, 0.2, 1)
        Clock.unschedule(self.update_timer)
        
        # Play stop sound
        sound = SoundLoader.load('assets/stop.wav')
        if sound:
            sound.play()
            
    def update_timer(self, dt):
        if self.current_time <= 0:
            self.complete_pose()
            return False
            
        self.current_time -= 1
        self.timer_label.text = str(self.current_time)
        
        # Handle warning time
        warning_time = int(self.warning_input.text)
        if self.current_time == warning_time:
            sound = SoundLoader.load('assets/warning.wav')
            if sound:
                sound.play()
                
        return True
        
    def randomize_pose(self, instance):
        if self.data_manager.poses:
            pose = random.choice(self.data_manager.poses)
            self.pose_label.text = pose['name']
            sound = SoundLoader.load('assets/randomize.wav')
            if sound:
                sound.play()

class MainApp(App):
    def build(self):
        data_manager = DataManager()
        return TimerScreen(data_manager)

if __name__ == '__main__':
    if platform == 'android':
        from android.permissions import request_permissions, Permission
        request_permissions([
            Permission.INTERNET,
            Permission.WRITE_EXTERNAL_STORAGE
        ])
    
    MainApp().run()
