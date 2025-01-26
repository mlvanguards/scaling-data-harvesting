"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

export default function Home() {
  const [urls, setUrls] = useState("");
  const [data, setData] = useState({ trends: [], summary_of_findings: "" });
  const [loading, setLoading] = useState(false);

  // const handleGenerate = async () => {
  //   // This is a placeholder function. In a real application, you'd call an API here.
  //   const urlList = urls.split("\n").filter((url) => url.trim() !== "");
  //   const placeholderText = `Generated text based on ${urlList.length} LinkedIn URL(s)`;
  //   setGeneratedText(placeholderText);
  // };

  type Trend = {
    title: string;
    why: string;
    recommendation: string;
  };

  type InsightSectionProps = {
    trends: Trend[];
    summary: string;
  };

  const InsightSection: React.FC<InsightSectionProps> = ({ trends, summary }) => {
    return (
      <div style={{ padding: "20px", fontFamily: "Arial, sans-serif", lineHeight: 1.6 }}>
        {trends.map((trend, index) => (
            <div key={index} style={{marginBottom: "20px"}}>
              <h2 style={{fontWeight: "bold"}}>{index + 1}. {trend.title}</h2>
              <p><strong>Why:</strong> {trend.why}</p>
              <p><strong>Recommendation:</strong> {trend.recommendation}</p>
            </div>
        ))}
        <h3 style={{marginTop: "40px" , fontWeight: "bold"}}>Summary of Findings: </h3>
        <p>{summary}</p>
      </div>
    );
  };



  const handleGenerate = async () => {
    setLoading(true);

    try {
      const response = await fetch("http://localhost:8083/.functions/function-scheduler", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({"links": urls.split("\n")}),
      });

      if (!response.ok) {
        throw new Error(response.statusText);
      }

      const result = await response.json();
      console.log(result)
      setData(result)
    } catch (error) {
      console.error("Error generating text:", error);
    } finally {
      setLoading(false); // End loading
    }
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
                disabled={loading} // Disable button while loading
                className={`w-full text-white font-semibold py-3 rounded-xl transition duration-200 transform ${
                  loading
                    ? "bg-gray-500 cursor-not-allowed"
                    : "bg-[#59359A] hover:scale-105"
                }`}
              >
                {loading ? (
                  <div className="flex items-center justify-center">
                    <span className="animate-spin mr-2 border-2 border-t-transparent border-white rounded-full w-4 h-4"></span>
                    Loading...
                  </div>
                ) : (
                  "Generate Analysis"
                )}
              </Button>
              {data && (
                <div className="mt-8 p-4 bg-muted rounded-lg">
                  <h2 className="text-xl font-semibold mb-2 text-muted-white">
                    Trend Analysis:
                  </h2>
                  <InsightSection
                    trends={data.trends}
                    summary={data.summary_of_findings}
                  />
                  {/*<p className="text-foreground">{generatedText}</p>*/}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
