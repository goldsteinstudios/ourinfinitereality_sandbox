import { useMotionStore } from '../../store/useMotionStore';
import { Step1CharacterSelection } from './Step1CharacterSelection';
import { Step2RadicalBreakdown } from './Step2RadicalBreakdown';
import { Step3ToolIdentification } from './Step3ToolIdentification';
import { Step4MotionImagination } from './Step4MotionImagination';
import { Step5GeometricPattern } from './Step5GeometricPattern';
import { Step6MathematicalRelationship } from './Step6MathematicalRelationship';
import { Step7ContextTesting } from './Step7ContextTesting';
import { Step8InsightsReview } from './Step8InsightsReview';
import { WizardNavigation } from './WizardNavigation';
import { SavedInsightsList } from './SavedInsightsList';

export function MotionDecoder() {
  const { currentStep, workingInsight } = useMotionStore();

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return <Step1CharacterSelection />;
      case 2:
        return <Step2RadicalBreakdown />;
      case 3:
        return <Step3ToolIdentification />;
      case 4:
        return <Step4MotionImagination />;
      case 5:
        return <Step5GeometricPattern />;
      case 6:
        return <Step6MathematicalRelationship />;
      case 7:
        return <Step7ContextTesting />;
      case 8:
        return <Step8InsightsReview />;
      default:
        return <Step1CharacterSelection />;
    }
  };

  return (
    <div className="h-full flex gap-4 p-6 bg-gray-900">
      {/* Left Panel: Wizard Steps */}
      <div className="flex-1 flex flex-col gap-4">
        {/* Progress Indicator */}
        <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
          <div className="flex items-center justify-between mb-2">
            <h2 className="text-xl font-bold text-white">
              Character Motion Decoder
            </h2>
            {workingInsight?.character && (
              <div className="text-2xl font-bold text-blue-400">
                {workingInsight.character}
              </div>
            )}
          </div>
          <div className="flex gap-2">
            {[1, 2, 3, 4, 5, 6, 7, 8].map((step) => (
              <div
                key={step}
                className={`flex-1 h-2 rounded ${
                  step === currentStep
                    ? 'bg-blue-500'
                    : step < currentStep
                    ? 'bg-blue-700'
                    : 'bg-gray-700'
                }`}
              />
            ))}
          </div>
          <div className="mt-2 text-sm text-gray-400">
            Step {currentStep} of 8: {getStepTitle(currentStep)}
          </div>
        </div>

        {/* Step Content */}
        <div className="flex-1 bg-gray-800 rounded-lg p-6 border border-gray-700 overflow-y-auto">
          {renderStep()}
        </div>

        {/* Navigation */}
        <WizardNavigation />
      </div>

      {/* Right Panel: Saved Insights */}
      <div className="w-80">
        <SavedInsightsList />
      </div>
    </div>
  );
}

function getStepTitle(step: number): string {
  const titles = {
    1: 'Character Selection',
    2: 'Radical Breakdown',
    3: 'Tool Identification',
    4: 'Motion Imagination',
    5: 'Geometric Pattern',
    6: 'Mathematical Relationship',
    7: 'Context Testing',
    8: 'Insights & Review',
  };
  return titles[step as keyof typeof titles] || '';
}
