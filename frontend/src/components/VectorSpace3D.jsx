// src/components/VectorSpace3D.jsx
import { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Points, PointMaterial } from '@react-three/drei';
import * as THREE from 'three';
import * as random from 'maath/random/dist/maath-random.esm';

function ControlledGalaxy({ appState }) {
  const pointsRef = useRef();
  const groupRef = useRef();
  
  // Generate 3500 points inside a wider field for a deep space effect
  const sphere = random.inSphere(new Float32Array(10500), { radius: 3.0 });

  useFrame((state, delta) => {
    if (!pointsRef.current || !groupRef.current) return;

    // 1. Dynamic Particle Rotation Speed adjustment based on state
    let rotationSpeed = delta / 20;
    if (appState === 'landing') rotationSpeed = delta / 5; // warp effect
    if (appState === 'auth') rotationSpeed = delta / 40;   // slow crawl

    pointsRef.current.rotation.y -= rotationSpeed;

    // 2. Camera Matrix Interpolation (Lerp) for smooth flight transitions
    const targetCameraPos = new THREE.Vector3(0, 0, 1.2);
    const targetGroupRot = new THREE.Vector3(0, 0, Math.PI / 4);

    if (appState === 'landing') {
      // Zoom out quickly from deep space on first landing
      targetCameraPos.set(0, 0, 0.4 + Math.sin(state.clock.getElapsedTime() * 0.5) * 0.1);
      targetGroupRot.set(state.clock.getElapsedTime() * 0.05, state.clock.getElapsedTime() * 0.02, 0);
    } else if (appState === 'auth') {
      // Shift off-center to comfortably place the floating login panel on the right side
      targetCameraPos.set(-0.4, 0, 1.4);
      targetGroupRot.set(0.2, -0.2, Math.PI / 6);
    } else if (appState === 'dashboard') {
      // Lock into a stable, rhythmic workspace orbit view
      targetCameraPos.set(0, 0, 1.6);
      targetGroupRot.set(Math.sin(state.clock.getElapsedTime() * 0.1) * 0.1, state.clock.getElapsedTime() * 0.01, 0);
    }

    // Apply the lerp smoothing functions fluidly across frames
    state.camera.position.lerp(targetCameraPos, 4 * delta);
    groupRef.current.rotation.x = THREE.MathUtils.lerp(groupRef.current.rotation.x, targetGroupRot.x, 3 * delta);
    groupRef.current.rotation.y = THREE.MathUtils.lerp(groupRef.current.rotation.y, targetGroupRot.y, 3 * delta);
    groupRef.current.rotation.z = THREE.MathUtils.lerp(groupRef.current.rotation.z, targetGroupRot.z, 3 * delta);
  });

  return (
    <group ref={groupRef}>
      <Points ref={pointsRef} positions={sphere} stride={3} frustumCulled={false}>
        <PointMaterial
          transparent
          color="#60a5fa"
          size={0.02}
          sizeAttenuation={true}
          depthWrite={false}
          blending={THREE.AdditiveBlending}
        />
      </Points>
    </group>
  );
}

export default function VectorSpace3D({ appState }) {
  return (
    <div className="absolute inset-0 z-0 bg-slate-950 pointer-events-none transition-all duration-1000">
      <Canvas camera={{ position: [0, 0, 2], fov: 60 }}>
        <ambientLight intensity={0.5} />
        <ControlledGalaxy appState={appState} />
      </Canvas>
    </div>
  );
}