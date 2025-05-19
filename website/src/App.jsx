import { BrowserRouter as Router, useLocation } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import Body from './components/Body';
import PrivacyPolicy from './components/PrivacyPolicy';
import { ThemeProvider } from './context/ThemeContext';

function AppContent() {
  const location = useLocation();
  const showPrivacyPolicy = location.pathname === '/privacy';

  return (
    <div className="flex min-h-screen flex-col">
      <Header />
      <Body />
      {showPrivacyPolicy && <PrivacyPolicy />}
      <Footer />
    </div>
  );
}

function App() {
  return (
    <Router>
      <ThemeProvider>
        <AppContent />
      </ThemeProvider>
    </Router>
  );
}

export default App;
