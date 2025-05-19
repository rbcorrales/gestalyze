import { useTranslation } from 'react-i18next';

function ResultView({ previewImage, isHandDetected, fingerCount, handView, handedness, liftedFingers, aslLetter, aslProbabilities }) {
  const { t } = useTranslation();

  const getFingerName = (index) => {
    const fingerKeys = ['thumb', 'index', 'middle', 'ring', 'pinky'];
    return t(`results.fingers.${fingerKeys[index]}`);
  };

  return (
    <div className="w-full md:w-1/2">
      <div className="bg-white p-4 rounded-lg shadow">
        <div className="flex justify-between items-center mb-3">
          <h2 className="font-bold text-lg">{t('results.title')}</h2>
          <div className={`flex items-center gap-2 px-3 py-1 rounded-full ${
            isHandDetected ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
          }`}>
            <div className={`w-2 h-2 rounded-full ${
              isHandDetected ? 'bg-green-500' : 'bg-red-500'
            }`}></div>
            <span className="text-sm font-medium">
              {t(isHandDetected ? 'results.handStatus.detected' : 'results.handStatus.notDetected')}
            </span>
          </div>
        </div>
        {previewImage ? (
          <img
            src={previewImage}
            alt="Preview"
            className="w-full aspect-video object-contain bg-black rounded"
          />
        ) : (
          <div className="w-full aspect-video bg-gray-100 rounded flex items-center justify-center text-gray-500">
            {t('results.waiting')}
          </div>
        )}
        <div className="mt-4 grid grid-cols-3 gap-4">
          <div className="text-sm text-gray-600">
            {t('results.fingersDetected')}: {fingerCount}
          </div>
          <div className="text-sm text-gray-600">
            {t('results.handDetected')}: {handedness ? t(`results.handedness.${handedness.toLowerCase()}`) : '-'}
          </div>
          <div className="text-sm text-gray-600">
            {t('results.handView')}: {handView ? t(`results.view.${handView.toLowerCase()}`) : '-'}
          </div>
        </div>
        <div className="mt-2 text-sm text-gray-600">
          {t('results.liftedFingers')}: {liftedFingers?.length > 0 ? liftedFingers.map(i => getFingerName(i)).join(', ') : '-'}
        </div>
        
        {/* ASL Prediction Section */}
        {aslLetter && (
          <div className="mt-4 border-t pt-4">
            <h3 className="font-semibold text-lg mb-2">{t('results.asl.title')}</h3>
            <div className="text-4xl font-bold text-center mb-2">{aslLetter}</div>
            {aslProbabilities && (
              <div className="text-sm text-gray-600">
                {t('results.asl.confidence')}: {(aslProbabilities[aslLetter] * 100).toFixed(1)}%
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default ResultView;
