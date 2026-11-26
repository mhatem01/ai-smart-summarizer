/* --------------------------------------------------------
 * Core Frontend Service
 * Domain: Engineering and Technology
 * Focus: Applied Mathematics and Artificial Intelligence
 * Field: Computer and Data Science
 * Created by: MOHAMED HATEM MOHAMED ABDELAZIZ MOHAMED 
 *           & EBRAHIM MOHAMED EBRAHIM HAMADA RASAD
 * -------------------------------------------------------- */

import { GoogleGenAI } from "@google/genai";
import { useState, useEffect } from "react";
import { IoSparkles } from "react-icons/io5";
import {
  HiClipboard,
  HiExclamationCircle,
  HiPencilAlt,
  HiCheck,
  HiVolumeUp,
  HiStop,
  HiUsers,
  HiArrowLeft,
  HiTrash,
} from "react-icons/hi";

function App() {
  const [text, setText] = useState("");
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [showTeamPage, setShowTeamPage] = useState(false);

  useEffect(() => {
    return () => {
      if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  const isArabic = (str) => /[\u0600-\u06FF]/.test(str);

  const countWords = (str) => {
    return str
      .trim()
      .split(/\s+/)
      .filter((word) => word.length > 0).length;
  };

  const countSentences = (str) => {
    return str
      .trim()
      .split(/[.!?؟]+/)
      .filter((sentence) => sentence.trim().length > 0).length;
  };

  const pluralize = (count, singular, plural) => {
    return count === 1 ? singular : plural;
  };

  const pasteText = async () => {
    try {
      const clipboardText = await navigator.clipboard.readText();
      setText(clipboardText);
      setError(null);
    } catch (err) {
      console.error("Failed to paste: ", err);
      setError("Failed to paste text. Please paste it manually using Ctrl+V.");
    }
  };

  const summarizeText = async () => {
    if (!text.trim()) {
      setError("Please enter some text to summarize.");
      return;
    }

    if (text.trim().length < 50) {
      setError(
        "Text is too short to summarize. Please enter at least 50 characters."
      );
      return;
    }

    const apiKey = import.meta.env.VITE_GEMINI_API_KEY?.trim();
    if (!apiKey) {
      setError(
        "API Key is missing! Please add VITE_GEMINI_API_KEY in your environment variables."
      );
      return;
    }

    handleStopSpeech();
    setLoading(true);
    setError(null);
    setSummary("");

    try {
      const ai = new GoogleGenAI({ apiKey });
      const models = [
        "gemini-3.5-flash-lite",
        "gemini-3.8-flash",
        "gemini-3.5-flash",
        "gemini-4-hydrogen",
      ];
      let success = false;
      let errorsList = [];

      const promptInstruction = isArabic(text)
        ? "لخّص النص التالي بأسلوب واضح ومختصر باللغة العربية:\n\n"
        : "Provide a concise, clear summary of the following text:\n\n";

      for (const modelName of models) {
        try {
          const response = await ai.models.generateContent({
            model: modelName,
            contents: promptInstruction + text,
          });

          if (response && response.text) {
            setSummary(response.text.trim());
            success = true;
            break;
          }
        } catch (err) {
          console.error(`Error with ${modelName}:`, err);
          errorsList.push(`${modelName}: ${err?.message || "Failed"}`);
        }
      }

      if (!success) {
        setError(`Google API Error -> ${errorsList[0] || "Unknown error"}`);
      }
    } catch (globalErr) {
      setError(`Connection Error: ${globalErr.message}`);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(summary);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("Failed to copy: ", err);
      setError("Failed to copy to clipboard. Please try again.");
    }
  };

  const handleSpeak = () => {
    if (!summary || !("speechSynthesis" in window)) return;

    if (isSpeaking) {
      handleStopSpeech();
      return;
    }

    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(summary);
    utterance.lang = isArabic(summary) ? "ar-SA" : "en-US";

    utterance.onend = () => {
      setIsSpeaking(false);
    };

    utterance.onerror = (event) => {
      console.error("SpeechSynthesisUtterance error", event);
      setIsSpeaking(false);
    };

    setIsSpeaking(true);
    window.speechSynthesis.speak(utterance);
  };

  const handleStopSpeech = () => {
    if ("speechSynthesis" in window) {
      window.speechSynthesis.cancel();
    }
    setIsSpeaking(false);
  };

  const clearAll = () => {
    handleStopSpeech();
    setText("");
    setSummary("");
    setError(null);
    setCopied(false);
  };

  if (showTeamPage) {
    return (
      <div
        data-theme="light"
        className="min-h-screen bg-gradient-to-br from-purple-100 via-blue-100 to-pink-100 flex items-center justify-center p-4"
      >
        <div className="card bg-base-100 shadow-2xl max-w-3xl w-full p-8 rounded-2xl border border-purple-200">
          <div className="text-center mb-6">
            <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent mb-4 flex items-center justify-center gap-2">
              <HiUsers className="text-purple-600" /> The Ingenium Core Team
            </h1>
            <div className="bg-purple-900 p-5 rounded-xl max-w-md mx-auto text-left border border-purple-950 shadow-inner">
              <div className="flex items-center gap-2 text-purple-200 font-bold mb-3">
                <span className="text-base">🌐</span> Project Technical Foundation:
              </div>
              <ul className="list-disc list-inside text-sm text-purple-100 font-semibold space-y-2 pl-2">
                <li>Engineering and Technology</li>
                <li>Applied Mathematics and Artificial Intelligence</li>
                <li>Computer and Data Science</li>
              </ul>
            </div>
          </div>

          <div className="space-y-4 my-8">
            <div className="p-5 bg-base-100 shadow-md border-l-4 border-purple-600 rounded-r-xl border border-base-200">
              <h2 className="font-bold text-purple-600 text-lg">
                MOHAMED HATEM MOHAMED ABDELAZIZ MOHAMED
              </h2>
              <p className="text-sm text-base-content/70 mt-1">
                Systems Architecture & Backend Security Core
              </p>
            </div>

            <div className="p-5 bg-base-100 shadow-md border-l-4 border-blue-600 rounded-r-xl border border-base-200">
              <h2 className="font-bold text-blue-600 text-lg">
                EBRAHIM MOHAMED EBRAHIM HAMADA RASAD
              </h2>
              <p className="text-sm text-base-content/70 mt-1">
                User Interface Integration & API Data Handlers
              </p>
            </div>
          </div>

          <div className="text-center mt-6">
            <button
              onClick={() => setShowTeamPage(false)}
              className="inline-flex items-center gap-2 text-sm font-semibold text-purple-600 hover:text-purple-800 transition-colors btn btn-ghost btn-sm"
            >
              <HiArrowLeft className="w-4 h-4" /> Back to Summarizer App
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      data-theme="light"
      className="min-h-screen bg-gradient-to-br from-purple-100 via-blue-100 to-pink-100"
    >
      <div className="container mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-4 bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent flex items-center justify-center gap-3">
            <IoSparkles className="text-purple-600 hidden sm:block" /> AI Text Summarizer
          </h1>
          <p className="text-xl text-base-content/70 font-medium">
            Powered by Google Gemini AI
          </p>
        </div>

        <div className="card bg-base-100 shadow-2xl max-w-5xl mx-auto">
          <div className="card-body p-6 md:p-8">
            <div className="mb-6">
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-3">
                <label className="text-lg font-bold flex items-center gap-2 text-base-content">
                  <HiPencilAlt className="text-purple-600 w-5 h-5" /> Enter Your Text
                </label>
                <div className="flex gap-2">
                  <button
                    onClick={pasteText}
                    className="btn btn-sm btn-outline btn-primary gap-1"
                  >
                    <HiClipboard className="w-4 h-4" /> Paste Text
                  </button>
                  {text && (
                    <button
                      onClick={clearAll}
                      className="btn btn-sm btn-outline btn-error gap-1"
                    >
                      <HiTrash className="w-4 h-4" /> Clear
                    </button>
                  )}
                </div>
              </div>

              <textarea
                className="textarea textarea-bordered w-full h-48 text-base focus:outline-none focus:border-purple-500"
                placeholder="Paste or type your long article, essay, or notes here (at least 50 characters)..."
                value={text}
                onChange={(e) => setText(e.target.value)}
                dir="auto"
              ></textarea>

              <div className="flex justify-between text-xs text-base-content/60 mt-2 font-medium">
                <span>
                  {countWords(text)} {pluralize(countWords(text), "word", "words")} ·{" "}
                  {countSentences(text)}{" "}
                  {pluralize(countSentences(text), "sentence", "sentences")}
                </span>
                <span>{text.length} characters</span>
              </div>
            </div>

            {error && (
              <div className="alert alert-error mb-6 shadow-md">
                <HiExclamationCircle className="w-6 h-6 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            <button
              onClick={summarizeText}
              disabled={loading || !text.trim()}
              className="btn btn-primary w-full text-lg bg-gradient-to-r from-purple-600 to-blue-600 border-none hover:from-purple-700 hover:to-blue-700 text-white shadow-lg"
            >
              {loading ? (
                <>
                  <span className="loading loading-spinner loading-md"></span>
                  Summarizing...
                </>
              ) : (
                <>
                  <IoSparkles className="w-5 h-5" /> Summarize Text
                </>
              )}
            </button>

            {summary && (
              <div className="mt-8 p-6 bg-purple-50 rounded-xl border border-purple-200 shadow-inner">
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-4">
                  <h2 className="text-xl font-bold text-purple-900 flex items-center gap-2">
                    <IoSparkles className="text-purple-600" /> AI Summary
                  </h2>
                  <div className="flex gap-2">
                    <button
                      onClick={handleSpeak}
                      className={`btn btn-sm ${
                        isSpeaking ? "btn-error" : "btn-secondary"
                      } gap-1`}
                    >
                      {isSpeaking ? (
                        <>
                          <HiStop className="w-4 h-4" /> Stop Audio
                        </>
                      ) : (
                        <>
                          <HiVolumeUp className="w-4 h-4" /> Listen
                        </>
                      )}
                    </button>

                    <button
                      onClick={copyToClipboard}
                      className="btn btn-sm btn-outline btn-primary gap-1"
                    >
                      {copied ? (
                        <>
                          <HiCheck className="w-4 h-4 text-success" /> Copied!
                        </>
                      ) : (
                        <>
                          <HiClipboard className="w-4 h-4" /> Copy
                        </>
                      )}
                    </button>
                  </div>
                </div>

                <p
                  className="text-base-content text-lg leading-relaxed whitespace-pre-line"
                  dir="auto"
                >
                  {summary}
                </p>
              </div>
            )}

            <div className="mt-10 pt-6 border-t border-base-200 text-center">
              <button
                onClick={() => setShowTeamPage(true)}
                className="btn btn-outline btn-accent btn-sm gap-2"
              >
                <HiUsers className="w-4 h-4" /> View Project Team & Details
              </button>
              <p className="text-xs text-base-content/50 mt-3">
                All Rights Reserved © Team #01 - CS Division 2026
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
