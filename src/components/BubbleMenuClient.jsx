"use client";

import BubbleMenu from './BubbleMenu';
import { useCallback } from 'react';

export default function BubbleMenuClient() {
  const handleMenuClick = useCallback((open) => {
    // noop for now — this runs in the client
    // console.log('menu open:', open);
  }, []);

  return (
    <BubbleMenu
      useFixedPosition={true}
      className="bubble-menu-top-right"
      style={{ right: '1.25rem', top: '1.25rem' }}
      menuBg="#ffffff"
      menuContentColor="#111"
      onMenuClick={handleMenuClick}
      items={undefined}
      logo={undefined}
    />
  );
}
