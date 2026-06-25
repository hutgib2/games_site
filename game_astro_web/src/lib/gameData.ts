import ChessImage from '../assets/thumbnails/chess_preview.png';
import ShooterImage from '../assets/thumbnails/shooter_preview.png';
import SurvivorImage from '../assets/thumbnails/survivor_preview.png';
import TriviaImage from '../assets/thumbnails/trivia_preview.png';

export const gameData = {
	chess: {	
		title: 'Chess Reboot',
		image: ChessImage,
		description: 'This is some placeholder text.',
		href: '/games/chess-reboot',
		hrefSuffix: 'chess-reboot',
	},
    trivia: {	
		title: 'Trivia',
		image: TriviaImage,
		description: 'This is some placeholder text.',
		href: '/games/trivia',
		hrefSuffix: 'trivia',
	},
    space_shooter: {	
		title: 'Space Shooter',
		image: ShooterImage,
		description: 'This is some placeholder text.',
		href: '/games/space-shooter',
		hrefSuffix: 'space-shooter',
	},
    vampire_survivor: {	
		title: 'Vampire Survivor',
		image: SurvivorImage,
		description: 'This is some placeholder text.',
		href: '/games/vampire-survivor',
		hrefSuffix: 'vampire-survivor',
	},
}
