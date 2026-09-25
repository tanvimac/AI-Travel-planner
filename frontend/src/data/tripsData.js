import tokyoImg from '../assets/tokyo.jpg';
import kyotoImg from '../assets/kyoto.jpg';

export const INITIAL_SAVED_TRIPS = [
  {
    id: 'tokyo-japan-1',
    destination: 'Tokyo, Japan',
    days: 7,
    travelers: 2,
    budget: 120000,
    formattedBudget: '$ 120,000',
    travelStyle: 'Luxury',
    tags: ['food', 'anime', 'Luxury'],
    createdAt: 'Sep 18, 2026',
    image: tokyoImg,
    description:
      'Experience the perfect blend of tradition and modernity in Tokyo — from world-class cuisine to anime culture, historic temples to vibrant city life.',
    highlights: [
      'Iconic landmarks',
      'Amazing food experiences',
      'Anime & pop culture',
      'Luxury accommodations',
    ],
    travelTips: [
      'Get a Japan Rail Pass (if traveling)',
      'Learn basic Japanese phrases',
      'Carry cash (some places don\'t accept cards)',
      'Check the weather and pack accordingly',
    ],
    itinerary: [
      {
        day: 1,
        title: 'Arrival in Tokyo',
        bullets: [
          'Check in to your hotel (Shinjuku)',
          'Evening stroll at Shinjuku Gyoen',
        ],
        image: 'https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=500&q=80',
      },
      {
        day: 2,
        title: 'Tokyo City Tour',
        bullets: [
          'Meiji Shrine',
          'Harajuku (shopping & food)',
          'Shibuya Crossing',
        ],
        image: 'https://images.unsplash.com/photo-1542051841857-5f90071e7989?auto=format&fit=crop&w=500&q=80',
      },
      {
        day: 3,
        title: 'Tsukiji Market & Ginza',
        bullets: [
          'Fresh seafood breakfast',
          'Explore Ginza shopping district',
        ],
        image: 'https://images.unsplash.com/photo-1554797589-7241bb691973?auto=format&fit=crop&w=500&q=80',
      },
      {
        day: 4,
        title: 'Asakusa & Akihabara Tech Culture',
        bullets: [
          'Historic Senso-ji Temple and Nakamise-dori shopping street',
          'Explore Akihabara electric town and anime collectibles',
          'Sumida River evening boat cruise',
        ],
        image: 'https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?auto=format&fit=crop&w=500&q=80',
      },
      {
        day: 5,
        title: 'Roppongi Arts & Odaiba Bay',
        bullets: [
          'Mori Art Museum and observation deck views',
          'TeamLab Planets digital interactive exhibition',
          'Rainbow Bridge sunset panorama',
        ],
        image: 'https://images.unsplash.com/photo-1536098561742-ca998e48cbcc?auto=format&fit=crop&w=500&q=80',
      },
      {
        day: 6,
        title: 'Kamakura & Enoshima Day Excursion',
        bullets: [
          'Marvel at Kotoku-in Great Buddha bronze monument',
          'Scenic Enoden coastal railway ride',
          'Seafood dinner overlooking Sagami Bay',
        ],
        image: 'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=500&q=80',
      },
      {
        day: 7,
        title: 'Omotesando & Michelin Farewell Dinner',
        bullets: [
          'Tree-lined Omotesando avenue and architecture tour',
          'Artisan souvenir & matcha confectionery tasting',
          'Celebratory multi-course Omakase dinner',
        ],
        image: 'https://images.unsplash.com/photo-1618773928121-c32242e63f39?auto=format&fit=crop&w=500&q=80',
      },
    ],
  },
  {
    id: 'kyoto-japan-2',
    destination: 'Kyoto, Japan',
    days: 5,
    travelers: 2,
    budget: 80000,
    formattedBudget: '$ 80,000',
    travelStyle: 'Mid-range',
    tags: ['culture', 'nature', 'Mid-range'],
    createdAt: 'Sep 18, 2026',
    image: kyotoImg,
    description:
      'Immerse yourself in Japan’s historic heart, adorned with thousands of classical Buddhist temples, Zen gardens, traditional wooden houses, and serene bamboo forests.',
    highlights: [
      'Fushimi Inari Torii path',
      'Traditional tea ceremony in Gion',
      'Arashiyama bamboo grove sunrise',
      'Authentic Kaiseki dining',
    ],
    travelTips: [
      'Rent an electric bicycle to glide through historic alleys',
      'Visit popular shrines early morning for quiet views',
      'Carry coins for bus fares and shrine fortune slips',
      'Wear comfortable slip-on shoes for temple entry',
    ],
    itinerary: [
      {
        day: 1,
        title: 'Arrival & Gion Lantern Walk',
        bullets: [
          'Check into traditional Machiya townhome',
          'Stroll through lantern-lit Hanami-koji street',
          'Sample delicate Kyoto tofu cuisine',
        ],
        image: 'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=500&q=80',
      },
      {
        day: 2,
        title: 'Fushimi Inari & Kiyomizu-dera',
        bullets: [
          'Hike through 10,000 vermilion Torii gates',
          'Visit historic Kiyomizu-dera cliffside stage',
          'Browse artisan pottery along Ninenzaka path',
        ],
        image: 'https://images.unsplash.com/photo-1545569341-9eb8b30979d9?auto=format&fit=crop&w=500&q=80',
      },
      {
        day: 3,
        title: 'Arashiyama Bamboo & Monkey Park',
        bullets: [
          'Early morning walk in tranquil Arashiyama Bamboo Grove',
          'Tenryu-ji UNESCO Zen landscaped gardens',
          'Panoramic views from Iwatayama Monkey Park',
        ],
        image: 'https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=500&q=80',
      },
      {
        day: 4,
        title: 'Golden Pavilion & Zen Rock Gardens',
        bullets: [
          'Marvel at mirror reflection of Kinkaku-ji (Golden Pavilion)',
          'Meditation at Ryoan-ji dry landscape rock garden',
          'Green matcha tea ceremony demonstration',
        ],
        image: 'https://images.unsplash.com/photo-1528360983277-13d401cdc186?auto=format&fit=crop&w=500&q=80',
      },
      {
        day: 5,
        title: 'Nijo Castle & Nishiki Food Market',
        bullets: [
          'Walk the squeaking nightingale floors of Nijo Castle',
          'Indulge in street foods across 400-year-old Nishiki Market',
          'Farewell sunset over Kamogawa River',
        ],
        image: 'https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?auto=format&fit=crop&w=500&q=80',
      },
    ],
  },
  {
    id: 'bali-indonesia-3',
    destination: 'Bali, Indonesia',
    days: 8,
    travelers: 2,
    budget: 70000,
    formattedBudget: '$ 70,000',
    travelStyle: 'Budget',
    tags: ['beach', 'adventure', 'Budget'],
    createdAt: 'Sep 17, 2026',
    image: 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=800&q=80',
    description:
      'A tropical sanctuary of dramatic ocean cliffs, sacred water temples, world-class surf breaks, emerald rice terraces, and warm Indonesian hospitality.',
    highlights: [
      'Uluwatu cliff temple & Kecak dance',
      'Tegalalang emerald rice terraces',
      'Snorkeling with manta rays in Nusa Penida',
      'Mount Batur sunrise volcano trek',
    ],
    travelTips: [
      'Use Gojek or Grab apps for reliable transport',
      'Always dress respectfully with a sarong at sacred temples',
      'Keep hydrated with fresh coconuts and bottled water',
      'Negotiate politely in local art and craft markets',
    ],
    itinerary: [
      {
        day: 1,
        title: 'Arrival in Canggu & Coastal Sunset',
        bullets: [
          'Check in to boutique eco-resort',
          'Sunset surfing watch at Echo Beach',
          'Dinner at beachfront organic cafe',
        ],
        image: 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=500&q=80',
      },
      {
        day: 2,
        title: 'Uluwatu Cliffs & Kecak Fire Show',
        bullets: [
          'Padang Padang beach swim and sunbathing',
          'Explore dramatic Uluwatu cliff temple',
          'Sunset Kecak fire dance performance',
        ],
        image: 'https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?auto=format&fit=crop&w=500&q=80',
      },
      {
        day: 3,
        title: 'Journey to Ubud & Sacred Monkey Forest',
        bullets: [
          'Scenic drive up to cultural haven Ubud',
          'Encounter playful macaques at Sacred Monkey Forest',
          'Stroll through Ubud Royal Palace',
        ],
        image: 'https://images.unsplash.com/photo-1555400038-63f5ba517a47?auto=format&fit=crop&w=500&q=80',
      },
      {
        day: 4,
        title: 'Tegalalang Rice Terraces & Tirta Empul',
        bullets: [
          'Sunrise stroll along Tegalalang rice terrace layers',
          'Holy spring water cleansing at Tirta Empul Temple',
          'Balinese coffee plantation tasting',
        ],
        image: 'https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=500&q=80',
      },
      {
        day: 5,
        title: 'Mount Batur Sunrise Volcano Trek',
        bullets: [
          'Early 3:00 AM guided hike up Mount Batur caldera',
          'Breakfast with steam-cooked eggs above the clouds',
          'Relaxing soak in Toya Devasya natural hot springs',
        ],
        image: 'https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?auto=format&fit=crop&w=500&q=80',
      },
      {
        day: 6,
        title: 'Nusa Penida Island Adventure',
        bullets: [
          'Speedboat across Badung Strait to Nusa Penida',
          'Breathtaking photo stop at Kelingking T-Rex cliff',
          'Snorkel alongside majestic manta rays in Crystal Bay',
        ],
        image: 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=500&q=80',
      },
      {
        day: 7,
        title: 'Seminyak Relaxation & Spa Day',
        bullets: [
          'Traditional Balinese herbal scrub and massage',
          'Boutique shopping along Seminyak Square',
          'Beach club daybed lounge and cocktails',
        ],
        image: 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=500&q=80',
      },
      {
        day: 8,
        title: 'Tanah Lot Sunset & Farewell Feast',
        bullets: [
          'Visit iconic sea temple Tanah Lot resting on ocean waves',
          'Shop handcrafted silver jewelry in Celuk',
          'Beachfront candlelit grilled seafood dinner in Jimbaran Bay',
        ],
        image: 'https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?auto=format&fit=crop&w=500&q=80',
      },
    ],
  },
];

// Helper to generate dynamic itinerary when a new trip is submitted
export function generateItineraryForTrip(tripData) {
  const daysCount = parseInt(tripData.days, 10) || 3;
  const destination = tripData.destination || 'Dream Destination';
  const travelStyle = tripData.travelStyle || 'Mid-range';
  const interestsList = tripData.interests
    ? tripData.interests.split(',').map((s) => s.trim()).filter(Boolean)
    : ['exploration', 'culture'];

  const tags = [...new Set([...interestsList.slice(0, 2), travelStyle])];

  const genericDailyPlans = [
    {
      title: `Arrival & Settling into ${destination}`,
      bullets: [
        `Check in to your hotel and unwind`,
        `Introductory neighborhood walking tour and orientation`,
        `Welcome dinner sampling authentic regional specialties`,
      ],
      image: 'https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=500&q=80',
    },
    {
      title: 'Iconic City Landmarks & Cultural Heritage',
      bullets: [
        'Guided tour of premier architectural landmarks & historic quarters',
        'Traditional marketplace exploration with local artisans',
        'Sunset scenic vista overlooking the city skyline',
      ],
      image: 'https://images.unsplash.com/photo-1542051841857-5f90071e7989?auto=format&fit=crop&w=500&q=80',
    },
    {
      title: 'Deep Dive into Food & Local Flavors',
      bullets: [
        'Morning street food tasting and market crawl',
        'Exclusive chef-led culinary workshop or dining experience',
        'Evening cultural performance or music lounge',
      ],
      image: 'https://images.unsplash.com/photo-1554797589-7241bb691973?auto=format&fit=crop&w=500&q=80',
    },
    {
      title: 'Nature Excursions & Scenic Escapes',
      bullets: [
        'Half-day excursion to nearby scenic nature reserves or gardens',
        'Panoramic outdoor picnic or waterfront lunch',
        'Leisurely afternoon exploring hidden boutique shops',
      ],
      image: 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=500&q=80',
    },
    {
      title: 'Arts, Museums & Modern Attractions',
      bullets: [
        'World-class museum or contemporary art gallery visit',
        'Specialty shopping and souvenir hunting',
        'Rooftop sunset cocktail lounge with panoramic vistas',
      ],
      image: 'https://images.unsplash.com/photo-1536098561742-ca998e48cbcc?auto=format&fit=crop&w=500&q=80',
    },
    {
      title: 'Day Trip to Charming Neighboring Villages',
      bullets: [
        'Scenic train or vehicle ride to nearby historic enclave',
        'Authentic regional lunch at a family-run heritage tavern',
        'Picturesque photography walk through cobblestone lanes',
      ],
      image: 'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=500&q=80',
    },
    {
      title: 'Final Day Highlights & Celebratory Farewell',
      bullets: [
        'Morning leisure at a signature local café',
        'Last-minute specialty gifts and keepsake shopping',
        'Celebratory multi-course dinner celebrating your journey',
      ],
      image: 'https://images.unsplash.com/photo-1618773928121-c32242e63f39?auto=format&fit=crop&w=500&q=80',
    },
  ];

  const itinerary = [];
  for (let i = 1; i <= daysCount; i++) {
    const planIndex = (i - 1) % genericDailyPlans.length;
    const base = genericDailyPlans[planIndex];
    itinerary.push({
      day: i,
      title: i === 1 ? `Arrival in ${destination}` : `${destination} - ${base.title}`,
      bullets: base.bullets,
      image: base.image,
    });
  }

  const budgetNum = Number(tripData.budget) || 10000;
  const formattedBudget = `$ ${budgetNum.toLocaleString()}`;

  // Image selector based on destination
  let tripImage = 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=800&q=80';
  const destLower = destination.toLowerCase();
  if (destLower.includes('tokyo') || destLower.includes('japan')) {
    tripImage = tokyoImg;
  } else if (destLower.includes('kyoto')) {
    tripImage = kyotoImg;
  } else if (destLower.includes('bali')) {
    tripImage = 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=800&q=80';
  } else if (destLower.includes('paris') || destLower.includes('france')) {
    tripImage = 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=800&q=80';
  } else if (destLower.includes('rome') || destLower.includes('italy')) {
    tripImage = 'https://images.unsplash.com/photo-1552832230-c0197dd311b5?auto=format&fit=crop&w=800&q=80';
  } else if (destLower.includes('new york') || destLower.includes('usa')) {
    tripImage = 'https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?auto=format&fit=crop&w=800&q=80';
  }

  return {
    id: `trip-${Date.now()}`,
    destination: tripData.destination,
    days: daysCount,
    travelers: parseInt(tripData.travelers, 10) || 1,
    budget: budgetNum,
    formattedBudget,
    travelStyle: tripData.travelStyle || 'Mid-range',
    tags,
    createdAt: new Date().toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    }),
    image: tripImage,
    description: `Experience the exceptional wonder and vibrant charm of ${destination} curated meticulously around ${tripData.travelStyle || 'tailored'} travel preferences and personalized activities.`,
    highlights: [
      `Iconic ${destination} landmarks`,
      `Signature food & dining experiences`,
      `${travelStyle} curated activities`,
      `Optimal routes and comfortable stays`,
    ],
    travelTips: [
      `Research local transit passes and digital travel cards`,
      `Learn simple greetings in the local language`,
      `Keep digital copies of all reservations & passports`,
      `Check seasonal weather forecasts before final packing`,
    ],
    itinerary,
  };
}
