import { useTranslation } from 'react-i18next';
import useCamera from '../hooks/useCamera';
import CONFIG from '../frontend_config';
import { CameraIcon, ClockIcon, LanguageIcon } from '@heroicons/react/24/outline';

function CameraView({ socket, isConnected, aslEnabled, onAslToggle, selectedModel, onModelChange }) {
  const { t } = useTranslation();
  const {
    cameras,
    selectedCamera,
    videoRef,
    cameraUpdateInterval,
    handleCameraChange,
    handleIntervalChange,
    incrementInterval,
    decrementInterval,
  } = useCamera(socket, isConnected);

  return (
    <div className="w-full md:w-1/2">
      <div className="bg-white p-4 rounded-lg shadow">
        <div className="flex justify-between items-center mb-3">
          <h2 className="font-bold text-lg">{t('camera.title')}</h2>
          <div className={`flex items-center gap-2 ${
            isConnected ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
          } px-3 py-1 rounded-full`}>
            <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
            <span className="text-sm font-medium">
              {isConnected ? t('camera.status.connected') : t('camera.status.disconnected')}
            </span>
          </div>
        </div>
        <video
          ref={videoRef}
          autoPlay
          playsInline
          className="w-full aspect-video object-contain bg-black rounded mb-4"
        />
        <div className="flex flex-col gap-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <CameraIcon className="h-8 w-8 text-gray-500 mr-2" />
              <select
                value={selectedCamera}
                onChange={handleCameraChange}
                disabled={!isConnected}
                className="bg-white border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5"
              >
                {cameras.map((camera) => (
                  <option key={camera.deviceId} value={camera.deviceId}>
                    {camera.label || `Camera ${camera.deviceId}`}
                  </option>
                ))}
              </select>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center">
                <ClockIcon className="h-8 w-8 text-gray-500 mr-2" />
                <div className="flex items-center gap-2">
                  <button
                    onClick={decrementInterval}
                    disabled={!isConnected || cameraUpdateInterval <= CONFIG.MIN_CAMERA_UPDATE_INTERVAL}
                    className="px-2 py-1 text-sm bg-gray-100 rounded hover:bg-gray-200 disabled:opacity-50"
                  >
                    -
                  </button>
                  <span className="text-sm">{cameraUpdateInterval}ms</span>
                  <button
                    onClick={incrementInterval}
                    disabled={!isConnected || cameraUpdateInterval >= CONFIG.MAX_CAMERA_UPDATE_INTERVAL}
                    className="px-2 py-1 text-sm bg-gray-100 rounded hover:bg-gray-200 disabled:opacity-50"
                  >
                    +
                  </button>
                </div>
              </div>
              <div className="flex items-center">
                <LanguageIcon className="h-8 w-8 text-gray-500 mr-2" title={t('camera.asl')} aria-label={t('camera.asl')} />
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    className="sr-only peer"
                    checked={aslEnabled}
                    onChange={onAslToggle}
                    disabled={!isConnected}
                  />
                  <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                </label>
              </div>
            </div>
          </div>
          {aslEnabled && (
            <div className="flex items-center">
              <select
                value={selectedModel}
                onChange={(e) => onModelChange(e.target.value)}
                disabled={!isConnected}
                className="bg-white border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 w-full"
              >
                {CONFIG.ASL.AVAILABLE_MODELS.map((model) => (
                  <option key={model.id} value={model.id}>
                    {model.name}
                  </option>
                ))}
              </select>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default CameraView; 