Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SetOutputToWaveFile("c:\Users\ganti\chart\AI automation\OmniMind AI\dummy_data\project_gamma_audio.wav")
$synth.Speak("Alright team, let us discuss Project Gamma. Our goal is to build a new frontend dashboard. David, your task is to design the UI components by next Wednesday. Sarah, please hook up the API endpoints by Friday. Emily will oversee the deployment. Let us make it happen.")
$synth.Dispose()
