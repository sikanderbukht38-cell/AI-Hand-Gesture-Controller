from pycaw.pycaw import AudioUtilities


class VolumeController:

    def __init__(self):

        device = AudioUtilities.GetSpeakers()

        self.volume = device.EndpointVolume

    def set_volume(self, level):

        level = max(0, min(100, level))

        self.volume.SetMasterVolumeLevelScalar(
            level / 100.0,
            None
        )

    def get_volume(self):

        return int(
            self.volume.GetMasterVolumeLevelScalar() * 100
        )

    def mute(self):

        self.volume.SetMute(1, None)

    def unmute(self):

        self.volume.SetMute(0, None)

    def is_muted(self):

        return bool(
            self.volume.GetMute()
        )