import { useState, useEffect, useRef } from 'react';
import { useTranslation } from 'react-i18next';
import Header from './components/Header';
import Footer from './components/Footer';
import CameraView from './components/CameraView';
import ResultView from './components/ResultView';
import CONFIG from './frontend_config';
import './i18n/i18n_config';

function App() {
  const { t } = useTranslation();
  const [previewImage, setPreviewImage] = useState(null);
  const [isHandDetected, setIsHandDetected] = useState(false);
  const [fingerCount, setFingerCount] = useState(0);
  const [handView, setHandView] = useState(null);
  const [handedness, setHandedness] = useState(null);
  const [socket, setSocket] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [liftedFingers, setLiftedFingers] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [aslEnabled, setAslEnabled] = useState(CONFIG.ASL.ENABLED);
  const [selectedModel, setSelectedModel] = useState(CONFIG.ASL.MODEL_TYPE);
  const [aslLetter, setAslLetter] = useState(null);
  const [aslProbabilities, setAslProbabilities] = useState(null);
  const [showAbout, setShowAbout] = useState(false);
  const [showPrivacy, setShowPrivacy] = useState(false);
  const aboutModalRef = useRef(null);
  const privacyModalRef = useRef(null);

  useEffect(() => {
    const connectWebSocket = () => {
      const ws = new WebSocket(CONFIG.WEBSOCKET_URL);

      ws.onopen = () => {
        console.log("🟢 WebSocket Connected");
        setIsConnected(true);
        setSocket(ws);
        // Send initial ASL state and model type
        ws.send(JSON.stringify({ 
          enable_asl: CONFIG.ASL.ENABLED,
          model_type: CONFIG.ASL.MODEL_TYPE
        }));
      };

      ws.onclose = () => {
        console.log("🔴 WebSocket Disconnected");
        setIsConnected(false);
        setSocket(null);
        setTimeout(connectWebSocket, 3000); // Attempt to reconnect
      };

      ws.onerror = (e) => {
        console.error("🔴 WebSocket Error:", e);
        setIsConnected(false);
        setSocket(null);
      };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.image_with_landmarks) {
          setPreviewImage(data.image_with_landmarks);
        }
        if (data.hand_detected !== undefined) {
          setIsHandDetected(data.hand_detected);
        }
        if (data.finger_count !== undefined) {
          setFingerCount(data.finger_count);
        }
        if (data.hand_view !== undefined) {
          setHandView(data.hand_view);
        }
        if (data.handedness !== undefined) {
          setHandedness(data.handedness);
        }
        if (data.lifted_fingers !== undefined) {
          setLiftedFingers(data.lifted_fingers);
        }
        if (data.asl_letter !== undefined) {
          setAslLetter(data.asl_letter);
        }
        if (data.asl_probabilities !== undefined) {
          setAslProbabilities(data.asl_probabilities);
        }
      };

      return () => {
        if (ws) {
          ws.close();
        }
      };
    };

    connectWebSocket(); // Initial connection

    return () => {
      if (socket) {
        socket.close();
      }
    };
  }, []); // Empty dependency array - only run once on mount

  const toggleModal = () => {
    setShowModal(!showModal);
  };

  const handleAslToggle = () => {
    const newAslEnabled = !aslEnabled;
    setAslEnabled(newAslEnabled);
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify({ 
        enable_asl: newAslEnabled,
        model_type: selectedModel
      }));
    }
  };

  const handleModelChange = (modelType) => {
    setSelectedModel(modelType);
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify({ 
        enable_asl: aslEnabled,
        model_type: modelType
      }));
    }
  };

  const handleAboutClick = () => {
    setShowAbout(true);
  };

  const handleClickOutsideAbout = (event) => {
    if (aboutModalRef.current && !aboutModalRef.current.contains(event.target)) {
      setShowAbout(false);
    }
  };

  const handleClickOutsidePrivacy = (event) => {
    if (privacyModalRef.current && !privacyModalRef.current.contains(event.target)) {
      setShowPrivacy(false);
    }
  };

  useEffect(() => {
    if (showAbout) {
      document.addEventListener('mousedown', handleClickOutsideAbout);
    } else {
      document.removeEventListener('mousedown', handleClickOutsideAbout);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutsideAbout);
    };
  }, [showAbout]);

  useEffect(() => {
    if (showPrivacy) {
      document.addEventListener('mousedown', handleClickOutsidePrivacy);
    } else {
      document.removeEventListener('mousedown', handleClickOutsidePrivacy);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutsidePrivacy);
    };
  }, [showPrivacy]);

  const togglePrivacy = () => {
    setShowPrivacy(!showPrivacy);
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Header onAboutClick={handleAboutClick} />
      <main className="flex-grow container mx-auto p-4">
        <h2 className="text-lg text-blue-800 text-center tracking-widest uppercase mb-6">{t('header.subtitle')}</h2>
        {!isConnected && (
          <div className="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 mb-8" role="alert">
            <p>{t('camera.status.disconnected')}</p>
          </div>
        )}
        <div className="flex flex-col md:flex-row justify-center items-start gap-8">
          <CameraView 
            socket={socket} 
            isConnected={isConnected} 
            aslEnabled={aslEnabled}
            onAslToggle={handleAslToggle}
            selectedModel={selectedModel}
            onModelChange={handleModelChange}
          />
          <ResultView 
            previewImage={previewImage} 
            isHandDetected={isHandDetected}
            fingerCount={fingerCount}
            handView={handView}
            handedness={handedness}
            liftedFingers={liftedFingers}
            aslLetter={aslLetter}
            aslProbabilities={aslProbabilities}
          />
        </div>
      </main>
      <Footer onAboutClick={handleAboutClick} onPrivacyClick={togglePrivacy} />

      {/* About Modal */}
      {showAbout && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
          <div ref={aboutModalRef} className="bg-white p-4 rounded-lg shadow-lg">
            <h2 className="font-bold text-lg text-black">{t('about.title')}</h2>
            <p className="mt-2 text-black">{t('about.description')}</p>
            <button onClick={() => setShowAbout(false)} className="mt-4 px-4 py-2 bg-blue-500 text-white rounded float-right">{t('about.close')}</button>
          </div>
        </div>
      )}

      {/* Privacy Policy Modal */}
      {showPrivacy && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
          <div ref={privacyModalRef} className="bg-white p-6 rounded-lg shadow-lg max-w-2xl w-full">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">{t('footer.privacyPolicy')}</h2>
            <div className="text-gray-600 mb-4 space-y-4">
              <p>{t('privacy.introduction')}</p>
              <h3 className="font-bold">{t('privacy.dataCollection')}</h3>
              <p>{t('privacy.dataCollectionText')}</p>
              <h3 className="font-bold">{t('privacy.dataUsage')}</h3>
              <p>{t('privacy.dataUsageText')}</p>
              <h3 className="font-bold">{t('privacy.dataProtection')}</h3>
              <p>{t('privacy.dataProtectionText')}</p>
            </div>
            <button
              onClick={togglePrivacy}
              className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
            >
              {t('about.close')}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
