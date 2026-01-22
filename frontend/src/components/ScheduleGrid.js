import { useState } from 'react';
import { Card } from './ui/card';

const DAYS = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'];
const TIME_SLOTS = [
  '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', 
  '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', 
  '22:00', '23:00', '00:00'
];

const ScheduleGrid = ({ schedule, onChange }) => {
  const toggleSlot = (day, time) => {
    const newSchedule = { ...schedule };
    if (!newSchedule[day]) {
      newSchedule[day] = [];
    }
    
    if (newSchedule[day].includes(time)) {
      newSchedule[day] = newSchedule[day].filter(t => t !== time);
      if (newSchedule[day].length === 0) {
        delete newSchedule[day];
      }
    } else {
      newSchedule[day].push(time);
    }
    
    onChange(newSchedule);
  };

  const isSelected = (day, time) => {
    return schedule[day]?.includes(time) || false;
  };

  return (
    <div className="overflow-x-auto" data-testid="schedule-grid">
      <div className="min-w-max">
        {/* Header */}
        <div className="flex gap-2 mb-2">
          <div className="w-20"></div>
          {DAYS.map(day => (
            <div key={day} className="w-16 text-center">
              <span className="text-xs font-medium text-muted-foreground">{day.slice(0, 3)}</span>
            </div>
          ))}
        </div>

        {/* Grid */}
        <div className="space-y-2">
          {TIME_SLOTS.map(time => (
            <div key={time} className="flex gap-2 items-center">
              <div className="w-20 text-xs text-muted-foreground text-right">{time}</div>
              {DAYS.map(day => (
                <button
                  key={`${day}-${time}`}
                  data-testid={`schedule-slot-${day}-${time}`}
                  type="button"
                  onClick={() => toggleSlot(day, time)}
                  className={`w-16 h-10 rounded-md border schedule-slot ${
                    isSelected(day, time)
                      ? 'bg-primary/20 border-primary/50 selected'
                      : 'bg-white/5 border-white/10'
                  }`}
                >
                  {isSelected(day, time) && (
                    <span className="text-primary text-xs font-bold">✓</span>
                  )}
                </button>
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ScheduleGrid;