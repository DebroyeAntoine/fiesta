import React, { useEffect, useRef } from 'react';
import { gsap } from 'gsap';

interface GlowButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  className?: string;
  variant?: 'purple' | 'blue' | 'green';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
}

const GlowButton: React.FC<GlowButtonProps> = ({ 
  children, 
  onClick, 
  className,
  variant = 'purple',
  size = 'md',
  disabled = false
}) => {
  const buttonRef = useRef<HTMLButtonElement>(null);
  const gradientRef = useRef<HTMLDivElement>(null);

  const variants = {
    purple: {
      from: 'from-purple-500',
      to: 'to-pink-500',
      background: 'bg-purple-600',
      shadow: 'shadow-purple-500/30',
      hover: 'hover:bg-purple-700',
      glow: 'bg-purple-300'
    },
    blue: {
      from: 'from-blue-500',
      to: 'to-cyan-500',
      background: 'bg-blue-600',
      shadow: 'shadow-blue-500/30',
      hover: 'hover:bg-blue-700',
      glow: 'bg-blue-300'
    },
    green: {
      from: 'from-green-500',
      to: 'to-emerald-500',
      background: 'bg-green-600',
      shadow: 'shadow-green-500/30',
      hover: 'hover:bg-green-700',
      glow: 'bg-green-300'
    }
  };

  const sizes = {
    sm: 'py-1.5 px-4 text-sm',
    md: 'py-2.5 px-6 text-base',
    lg: 'py-3 px-8 text-lg'
  };

  useEffect(() => {
    const button = buttonRef.current;
    const gradient = gradientRef.current;
    if (!button || !gradient || disabled) return;

    const handlePointerMove = (e: PointerEvent) => {
      const rect = button.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;

      const distance = Math.sqrt(
        Math.pow(x - centerX, 2) + Math.pow(y - centerY, 2)
      );
      const maxDistance = Math.sqrt(
        Math.pow(rect.width / 2, 2) + Math.pow(rect.height / 2, 2)
      );
      const intensity = 1 - Math.min(distance / maxDistance, 1);

      gsap.to(button, {
        "--pointer-x": `${x}px`,
        "--pointer-y": `${y}px`,
        "--glow-opacity": intensity * 0.5,
        duration: 0.3,
        ease: "power2.out"
      });

      const rotationX = ((y - centerY) / rect.height) * 10;
      const rotationY = ((x - centerX) / rect.width) * 10;

      gsap.to(gradient, {
        rotateX: -rotationX,
        rotateY: rotationY,
        duration: 0.3,
        ease: "power2.out"
      });
    };

    const handlePointerLeave = () => {
      gsap.to(button, {
        "--glow-opacity": 0,
        duration: 0.3,
        ease: "power2.out"
      });

      gsap.to(gradient, {
        rotateX: 0,
        rotateY: 0,
        duration: 0.5,
        ease: "elastic.out(1, 0.5)"
      });
    };

    button.addEventListener("pointermove", handlePointerMove);
    button.addEventListener("pointerleave", handlePointerLeave);

    return () => {
      button.removeEventListener("pointermove", handlePointerMove);
      button.removeEventListener("pointerleave", handlePointerLeave);
    };
  }, [disabled]);

  return (
    <button
      ref={buttonRef}
      onClick={onClick}
      disabled={disabled}
      className={`
        relative w-full rounded-full overflow-hidden transition-all duration-300
        shadow-lg ${variants[variant].shadow}
        ${disabled ? 'opacity-50 cursor-not-allowed' : 'hover:scale-[1.02] hover:shadow-xl'}
        group ${className || ''}
      `}
      style={{ 
        '--pointer-x': '0px',
        '--pointer-y': '0px',
        '--glow-opacity': '0',
        perspective: '1000px'
      } as React.CSSProperties}
    >
      {/* Gradient background with rotation */}
      <div 
        ref={gradientRef}
        className="absolute inset-0 overflow-hidden rounded-full"
      >
        <div 
          className={`
            absolute inset-[-2px] bg-gradient-to-r ${variants[variant].from} ${variants[variant].to}
            opacity-75 group-hover:opacity-100 transition-opacity duration-300
            animate-spin
          `}
        />
      </div>

      {/* Main content container */}
      <span className={`
        relative block ${variants[variant].background} rounded-full
        ${sizes[size]} font-semibold text-white
        ${variants[variant].hover} transition-colors duration-300
        ${disabled ? '' : 'transform-gpu'}
      `}>
        {/* Glow effect */}
        <div 
          className={`
            absolute w-32 h-32 -left-16 -top-16 rounded-full blur-2xl
            transition-opacity duration-300 ${variants[variant].glow}
          `}
          style={{
            transform: `translate(var(--pointer-x, 0px), var(--pointer-y, 0px)) translateZ(0)`,
            opacity: 'var(--glow-opacity)',
          }}
        />

        {/* Shine effect */}
        <div 
          className={`
            absolute inset-0 opacity-0 group-hover:opacity-20
            transition-opacity duration-300
            bg-gradient-to-r from-transparent via-white to-transparent
            animate-shine
          `}
        />

        {/* Button text */}
        <span className="relative z-10">{children}</span>
      </span>
    </button>
  );
};

export default GlowButton;
