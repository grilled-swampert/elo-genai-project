import { useRef, useState } from "react";
import { TiLocationArrow } from "react-icons/ti";

const BentoTilt = ({ children, className = "" }) => {
  const [transformStyle, setTransformStyle] = useState("");
  const itemRef = useRef();

  const handleMouseMove = (e) => {
    if (!itemRef.current) return;

    const { left, top, width, height } = itemRef.current.getBoundingClientRect();

    const relativeX = (e.clientX - left) / width;
    const relativeY = (e.clientY - top) / height;

    const tiltY = 20 * (0.5 - relativeX);
    const tiltX = 20 * (0.5 - relativeY);

    const newTransformStyle = `perspective(700px) rotateX(${tiltX}deg) rotateY(${tiltY}deg) scale3d(0.97, 0.97, 0.97)`;

    setTransformStyle(newTransformStyle);
  };

  const handleMouseLeave = () => {
    setTransformStyle("");
  };

  return (
    <div
      className={className}
      ref={itemRef}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      style={{ transform: transformStyle }}
    >
      {children}
    </div>
  );
};

const Features = () => {
  const BentoCard = ({ src, title, description, isComingSoon }) => {
    return (
      <div className="relative size-full">
        <video
          src={src}
          loop
          muted
          autoPlay
          className="absolute left-0 top-0 size-full object-cover object-center"
        />
        <div className="relative z-10 flex size-full flex-col justify-between p-5 text-blue-50">
          <div>
            <h1 className="bento-title special-font">{title}</h1>
            {description && (
              <p className="mt-3 max-w-64 text-xs md:text-base">
                {description}
              </p>
            )}
          </div>
        </div>
      </div>
    );
  };

  return (
    <section className="bg-black pb-52" id="news">
      <div className="container mx-auto px-3 md:px-10">
        <BentoTilt className="border-hsla relative me-4 mb-7 h-96 w-full overflow-hidden rounded-md md:h-[65vh]">
          <BentoCard
            src="videos/new.webm"
            title={
              <>
                radia<b>n</b>t
              </>
            }
            description="India's economy continues to demonstrate resilience, with strong growth driven by manufacturing, infrastructure, and digital transformation. The government’s focus on self-reliance (Aatmanirbhar Bharat) and structural reforms has bolstered investor confidence, attracting FDI and fostering innovation across sectors."
            isComingSoon={true}
          />
        </BentoTilt>
        <div className="grid h-[135vh] me-4 grid-cols-2 grid-rows-1 gap-7">
          <BentoTilt className="bento-tlt_1 row-span-1 md:col-span-1 sm:col-span-2">
            <BentoCard
              src="videos/3.mp4"
              title={
                <>
                  radia<b>n</b>t
                </>
              }
              description="Mutual funds in India continue to grow in popularity, with SIP (Systematic Investment Plan) inflows reaching record highs. Retail investors are increasingly opting for equity and hybrid funds for long-term wealth creation, while thematic funds (e.g., green energy, AI, and healthcare) are gaining traction due to India's evolving investment landscape."
              isComingSoon={true}
            />
          </BentoTilt>
          <BentoTilt className="bento-tlt_1 me-4 md:col-span-1 sm:col-span-2">
            <BentoCard
              src="videos/2.mp4"
              title={
                <>
                  radia<b>n</b>t
                </>
              }
              description="India's stock markets, led by the Nifty and Sensex, are witnessing robust performance despite global economic challenges. Sectors like IT, banking, and renewable energy are driving growth, with increased participation from retail investors and rising trends in sustainable investing (ESG-focused portfolios"
              isComingSoon={true}
            />
          </BentoTilt>
        </div>
      </div>
    </section>
  );
};

export default Features;