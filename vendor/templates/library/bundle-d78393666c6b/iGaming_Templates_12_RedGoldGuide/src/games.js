// Optional game-artwork galleries, cropped from owner-supplied lobby screenshots.
// Put screenshots in assets-src/owner/<shot>.png, record each grid's tile bounds in GRIDS
// (find them with any image editor), then list games as [title, shot, row, col].
// Only list titles legible on the artwork; skip duplicates, blurred tiles and real people.
// Empty = the homepage and Permainan Slot page show no game gallery.
export const GAME_SHOTS_DATE = '2026-11-01';

export const GRIDS = {
  // 3: { cols: [[13, 388], [404, 780]], rows: [[20, 308], [326, 699]] },
};

export const GAME_GROUPS = [
  // { name: 'Slots', games: [['Game Title', 3, 0, 0], ['Other Game', 3, 0, 1]] },
].map((g) => ({
  ...g,
  games: g.games.map(([title, shot, row, col]) => ({
    title, shot, row, col,
    file: title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''),
  })),
}));
