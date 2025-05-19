import { useState, useEffect, useRef } from 'react';
import { setCookie, getCookie } from '../utils/cookies';
import CONFIG from '../frontend_config';

const useCamera = (socket, isConnected) => {
  const [cameras, setCameras] = useState([]);
  const [selectedCamera, setSelectedCamera] = useState('');
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const intervalRef = useRef(null);
  const [cameraUpdateInterval, setCameraUpdateInterval] = useState(CONFIG.DEFAULT_CAMERA_UPDATE_INTERVAL);

  useEffect(() => {
    getCameras();
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  useEffect(() => {
    if (isConnected && selectedCamera) {
      startCamera(selectedCamera);
    }
  }, [isConnected]);

  const getCameras = async () => {
    try {
      const devices = await navigator.mediaDevices.enumerateDevices();
      const videoDevices = devices.filter(device => device.kind === "videoinput");
      setCameras(videoDevices);

      const savedDeviceId = getCookie("preferredCamera");
      let defaultIndex = 0;

      if (savedDeviceId) {
        const index = videoDevices.findIndex(device => device.deviceId === savedDeviceId);
        if (index !== -1) defaultIndex = index;
      } else {
        defaultIndex = Math.min(1, videoDevices.length - 1);
      }

      if (videoDevices.length > 0) {
        setSelectedCamera(videoDevices[defaultIndex].deviceId);
        startCamera(videoDevices[defaultIndex].deviceId);
      }
    } catch (error) {
      console.error("Error listing cameras:", error);
    }
  };

  const startCamera = async (deviceId) => {
    try {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }

      const constraints = {
        video: {
          width: { ideal: 1920 },
          height: { ideal: 1080 },
          aspectRatio: 16 / 9
        }
      };

      if (deviceId) {
        constraints.video.deviceId = { exact: deviceId };
      }

      const stream = await navigator.mediaDevices.getUserMedia(constraints);

      videoRef.current.srcObject = stream;
      streamRef.current = stream;

      await new Promise((resolve) => {
        videoRef.current.onloadedmetadata = () => {
          videoRef.current.play();
          resolve();
        };
      });

      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d");

      // Clear the previous interval if it exists
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }

      // Create a new interval with the updated camera update interval
      intervalRef.current = setInterval(() => {
        if (!videoRef.current || !isConnected || !socket) {
          return;
        }

        try {
          canvas.width = videoRef.current.videoWidth;
          canvas.height = videoRef.current.videoHeight;
          ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
          const imageData = canvas.toDataURL("image/jpeg", 0.8);
          
          socket.send(JSON.stringify({ image: imageData }));
        } catch (error) {
          console.error("Error sending frame:", error);
        }
      }, cameraUpdateInterval); // Use the interval from state

    } catch (error) {
      console.error("Error accessing camera:", error);
    }
  };

  const handleCameraChange = (e) => {
    const deviceId = e.target.value;
    setSelectedCamera(deviceId);
    setCookie("preferredCamera", deviceId, 30);
    startCamera(deviceId);
  };

  const handleIntervalChange = (e) => {
    const value = Math.max(CONFIG.MIN_CAMERA_UPDATE_INTERVAL, Math.min(CONFIG.MAX_CAMERA_UPDATE_INTERVAL, parseInt(e.target.value, 10) || 0));
    setCameraUpdateInterval(value);
    
    // Clear the previous interval and create a new one with the updated value
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      startCamera(selectedCamera); // Restart the camera with the new interval
    }
  };

  const incrementInterval = () => {
    setCameraUpdateInterval(prev => {
      const newValue = Math.min(prev + CONFIG.CAMERA_UPDATE_INTERVAL_STEP, CONFIG.MAX_CAMERA_UPDATE_INTERVAL);
      // Clear the previous interval and create a new one with the updated value
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        startCamera(selectedCamera); // Restart the camera with the new interval
      }
      return newValue;
    });
  };

  const decrementInterval = () => {
    setCameraUpdateInterval(prev => {
      const newValue = Math.max(prev - CONFIG.CAMERA_UPDATE_INTERVAL_STEP, CONFIG.MIN_CAMERA_UPDATE_INTERVAL);
      // Clear the previous interval and create a new one with the updated value
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        startCamera(selectedCamera); // Restart the camera with the new interval
      }
      return newValue;
    });
  };

  return {
    cameras,
    selectedCamera,
    setSelectedCamera,
    videoRef,
    cameraUpdateInterval,
    setCameraUpdateInterval,
    handleCameraChange,
    handleIntervalChange,
    incrementInterval,
    decrementInterval,
    isConnected,
  };
};

export default useCamera;
