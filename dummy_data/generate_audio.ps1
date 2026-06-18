Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SetOutputToWaveFile("c:\Users\ganti\chart\AI automation\OmniMind AI\dummy_data\project_delta_security.wav")
$synth.Speak("Hello team. Let's kick off the Project Delta sync. We need to completely overhaul the security architecture. Michael, your task is to implement the OAuth2 flow by Monday. Jessica, please audit the current database roles and permissions by Wednesday. Brian, you need to write the security documentation before Friday. Thank you.")
$synth.Dispose()
