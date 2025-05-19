import Header from './components/Header';
import Footer from './components/Footer';
import Body from './components/Body';
import { ThemeProvider } from './context/ThemeContext';

function App() {
  return (
    <ThemeProvider>
      <div className="flex min-h-screen flex-col">
        <Header />
        <Body />
        <Footer />
      </div>
    </ThemeProvider>
  );
}

export default App;
