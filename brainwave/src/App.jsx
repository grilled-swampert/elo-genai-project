import ButtonGradient from "./assets/svg/ButtonGradient";
import Benefits from "./components/Benefits";
import Features from "./components/Features";
import Chatbot from "./components/Chatbot";
import Hero from "./components/Hero";
// import News from "./components/News";
import Footer from "./components/Footer";
import Header from "./components/Header";

const App = () => {
  return (
    <>
      <div className="pt-[4.75rem] lg:pt-[5.25rem] overflow-hidden">
        <Header />
        <Hero />
        {/* <News/> */}
        <Features />
        <Chatbot/>
        <Benefits />
        <Footer />
      </div>

      <ButtonGradient />
    </>
  );
};

export default App;
