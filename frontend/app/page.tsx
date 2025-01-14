"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

export default function Home() {
  const [urls, setUrls] = useState("");
  const [generatedText, setGeneratedText] = useState("");

  const handleGenerate = async () => {
    // This is a placeholder function. In a real application, you'd call an API here.
    const urlList = urls.split("\n").filter((url) => url.trim() !== "");
    const placeholderText = `Generated text based on ${urlList.length} LinkedIn URL(s)`;
    setGeneratedText(placeholderText);
  };

  return (
    <div
      className="relative min-h-screen flex flex-col items-center bg-[#21143a] text-white"
      style={{
        background:
          "radial-gradient(circle, rgba(33, 20, 58, 0.95) 0%, rgba(33, 20, 58, 1) 100%)",
      }}
    >
      <div className="absolute inset-0 h-[94px] border-b-[1px] border-[#ffffff1a]"></div>

      <div className="container min-h-screen pt-36 border-x-[1px] h-full border-[#ffffff1a]">
        <div className="h-full overflow-auto">
          <div className="p-4 sm:p-6 md:p-8 flex items-center justify-center">
            <div className="w-full max-w-2xl space-y-8 bg-[#ffffff12] p-6 sm:p-8 rounded-tr-2xl rounded-bl-2xl shadow-lg">
              <h1 className="text-3xl sm:text-4xl font-extrabold text-primary bg-clip-text">
                Trending on Linkedin
              </h1>
              <Textarea
                placeholder="Enter LinkedIn URLs (one per line)"
                value={urls}
                onChange={(e) => setUrls(e.target.value)}
                className="w-full h-32 bg-input text-foreground border border-border rounded-md placeholder-muted-foreground focus:border-primary focus:ring-primary transition duration-200"
              />
              <Button
                onClick={handleGenerate}
                className="w-full bg-[#59359A] text-white font-semibold py-3 rounded-xl transition duration-200 transform hover:scale-105 "
              >
                Generate Analysis
              </Button>
              {generatedText && (
                <div className="mt-8 p-4 bg-muted rounded-lg">
                  <h2 className="text-xl font-semibold mb-2 text-muted-white">
                    Trend Analysis:
                  </h2>
                  <RawTextFormatter />
                  <p className="text-foreground">{generatedText}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
