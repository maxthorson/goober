"use client";

import BubbleMenu from './BubbleMenu';
import { useCallback } from 'react';
import Link from 'next/link';

export default function BubbleMenuClient() {
  const handleMenuClick = useCallback((open) => {
    // noop for now — this runs in the client
  }, []);

  const logo = (
    <Link href="/" className="text-sm font-semibold text-black no-underline">
      goober
    </Link>
  );

  return (
    <BubbleMenu
      useFixedPosition={true}
      className="bubble-menu-top-right"
      style={{ right: '1.25rem', top: '1.25rem' }}
      menuBg="#ffffff"
      menuContentColor="#111"
      onMenuClick={handleMenuClick}
      items={undefined}
      logo={logo}
    />
  );
}
