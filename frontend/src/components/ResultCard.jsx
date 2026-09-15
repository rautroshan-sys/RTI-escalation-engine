import React from 'react';

const ResultCard = ({ result }) => {
  if (!result) return null;

  const isEscalated = result.decision === "ESCALATE";
  const topPrediction = result.predictions[0];
  const secondPrediction = result.predictions[1];

  return (
    <div className={`p-6 rounded-xl shadow-lg border-2 ${isEscalated ? 'border-amber-500 bg-amber-50' : 'border-emerald-500 bg-emerald-50'}`}>
      
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold text-gray-800">Routing Decision</h2>
        <span className={`px-4 py-1 rounded-full font-bold text-white ${isEscalated ? 'bg-amber-500' : 'bg-emerald-500'}`}>
          {result.decision.replace('_', ' ')}
        </span>
      </div>

      {isEscalated && (
        <div className="mb-6 p-4 bg-white rounded-lg border-l-4 border-amber-500 shadow-sm">
          <p className="text-sm font-semibold text-amber-800 uppercase tracking-wider">Section 6(3) Escalation Triggered</p>
          <p className="text-gray-700 mt-1">{result.escalation_reason}</p>
        </div>
      )}

      <div className="space-y-4 bg-white p-4 rounded-lg shadow-sm">
        <h3 className="text-sm font-semibold text-gray-500 uppercase">AI Confidence Scores</h3>
        
        <div>
          <div className="flex justify-between text-sm font-medium mb-1">
            <span>{topPrediction.department_id} (Top Match)</span>
            <span>{(topPrediction.confidence_score * 100).toFixed(1)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2.5">
            <div className={`h-2.5 rounded-full ${isEscalated ? 'bg-amber-400' : 'bg-emerald-500'}`} style={{ width: `${topPrediction.confidence_score * 100}%` }}></div>
          </div>
        </div>

        <div>
          <div className="flex justify-between text-sm font-medium mb-1 text-gray-500">
            <span>{secondPrediction.department_id}</span>
            <span>{(secondPrediction.confidence_score * 100).toFixed(1)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2.5">
            <div className="bg-gray-400 h-2.5 rounded-full" style={{ width: `${secondPrediction.confidence_score * 100}%` }}></div>
          </div>
        </div>
      </div>

      {isEscalated && result.appeal_pathway && (
        <div className="mt-6 p-4 bg-gray-800 rounded-lg text-white shadow-sm">
          <h3 className="text-sm font-semibold uppercase text-gray-300 mb-2">Recommended Next Steps</h3>
          <p className="text-sm"><span className="font-bold">Authority:</span> {result.appeal_pathway.appellate_authority}</p>
          <p className="text-sm mt-1"><span className="font-bold">Timeline:</span> {result.appeal_pathway.statutory_timeline_days} Days</p>
        </div>
      )}

      <div className="mt-4 text-xs text-gray-400 text-right">
        Transaction ID: {result.transaction_id}
      </div>
    </div>
  );
};

export default ResultCard;