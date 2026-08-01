# Translation Studio - Tao Te Ching

## Overview

This is a modern web application designed for translating classical Chinese texts, specifically the Tao Te Ching. The application provides a comprehensive translation studio with character-by-character mapping capabilities, progress tracking, and multi-layered translation approaches (literal, philosophical, and contextual).

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite for fast development and optimized builds
- **Styling**: Tailwind CSS with custom design system
- **UI Components**: Radix UI primitives with shadcn/ui component library
- **State Management**: TanStack Query (React Query) for server state
- **Routing**: Wouter for lightweight client-side routing

### Backend Architecture
- **Runtime**: Node.js with Express.js
- **Language**: TypeScript with ES modules
- **API Pattern**: RESTful API with JSON responses
- **Error Handling**: Centralized error middleware with proper HTTP status codes
- **Development**: Hot module replacement via Vite integration

### Database & ORM
- **Database**: PostgreSQL (configured for Neon serverless)
- **ORM**: Drizzle ORM with type-safe queries
- **Schema Management**: Drizzle Kit for migrations
- **Connection**: @neondatabase/serverless driver for edge compatibility

## Key Components

### Core Entities
1. **Chapters**: Chinese text with pinyin, title, and chapter numbering
2. **Characters**: Individual Chinese characters with frequency tracking
3. **Mappings**: Translation mappings with literal, philosophical, and contextual interpretations
4. **Chapter Progress**: Completion tracking per chapter

### Frontend Components
- **TranslationStudio**: Main application interface
- **ChapterSidebar**: Chapter navigation with progress indicators
- **OriginalTextPanel**: Chinese text display with character selection
- **TranslationPanel**: Generated translation view
- **MappingPanel**: Character translation interface
- **ExportModal**: Translation export functionality

### Backend Services
- **Storage Interface**: Abstracted data access layer
- **Route Handlers**: RESTful endpoints for CRUD operations
- **Validation**: Zod schemas for request/response validation

## Data Flow

1. **Chapter Selection**: User selects a chapter from the sidebar
2. **Character Interaction**: Click on Chinese characters to create/edit mappings
3. **Translation Input**: Provide literal, philosophical, and contextual translations
4. **Progress Tracking**: Automatic calculation of completion percentages
5. **Real-time Updates**: TanStack Query manages cache invalidation and updates

## External Dependencies

### Core Dependencies
- **@neondatabase/serverless**: PostgreSQL connection for serverless environments
- **drizzle-orm**: Type-safe database queries
- **@tanstack/react-query**: Server state management
- **@radix-ui/***: Accessible UI primitives
- **express**: Backend web framework
- **zod**: Runtime type validation

### Development Tools
- **vite**: Build tool and dev server
- **tsx**: TypeScript execution for Node.js
- **tailwindcss**: Utility-first CSS framework
- **@replit/vite-plugin-***: Replit-specific development enhancements

## Deployment Strategy

### Build Process
- Frontend: Vite builds React app to `dist/public`
- Backend: esbuild bundles Node.js server to `dist/index.js`
- Single deployment artifact containing both frontend and backend

### Environment Configuration
- **Development**: `npm run dev` starts both frontend and backend with HMR
- **Production**: `npm run build && npm start` for optimized deployment
- **Database**: Requires `DATABASE_URL` environment variable

### Hosting Considerations
- Designed for Replit deployment with integrated development tools
- Compatible with any Node.js hosting platform
- PostgreSQL database can be hosted separately (Neon, Railway, etc.)

The application follows a monorepo structure with clear separation between client, server, and shared code, making it maintainable and scalable for translation workflow requirements.